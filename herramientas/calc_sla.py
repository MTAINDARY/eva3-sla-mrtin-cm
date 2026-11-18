#!/usr/bin/env python3
"""Calculadora reproducible EVA3. Solo procesa evidencias del enunciado; no son capturas de red.

Separa observación, validación de cobertura y derecho contractual a crédito.
"""
from __future__ import annotations
import argparse
import csv
import json
from datetime import datetime
from decimal import Decimal, getcontext
from pathlib import Path
import yaml

getcontext().prec = 28
D = lambda value: Decimal(str(value))


def cargar_csv(ruta):
    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


def intervalo_minutos(fecha, inicio, fin):
    a = datetime.fromisoformat(fecha + "T" + inicio)
    b = datetime.fromisoformat(fecha + "T" + fin)
    if b < a:
        from datetime import timedelta
        b += timedelta(days=1)
    return int((b-a).total_seconds() // 60)


def evaluar(obj, eventos, tickets, mediciones):
    mes = D(obj["minutos_mes"])
    min_cobertura = D(obj["minimo_cobertura"])
    lista_eventos, total_fisico, total_atribuible = [], D(0), D(0)
    estados = {}
    for e in eventos:
        minutos = D(intervalo_minutos(e["fecha"], e["inicio"], e["fin"]))
        es_atribuible = e["clasificacion"] == "atribuible"
        total_fisico += minutos
        if es_atribuible:
            total_atribuible += minutos
        lista_eventos.append({"evento":e["id"],"minutos":int(minutos),"atribuible":es_atribuible,
                              "fundamento":e["justificacion"],"clausula":e["referencia"]})
        estados[e["id"]] = (es_atribuible, minutos)
    disponibilidad = (mes-total_atribuible)/mes*D(100)
    permitidos = mes*(D(1)-D(obj["objetivos"]["disponibilidad"]["valor"])/D(100))
    def muestras(met):
        return [m for m in mediciones if m["metrica"] == met and m["valida_para_sla"] == "si"]
    lat = muestras("latencia")
    assert len(lat)==1, "Debe existir un único agregado de latencia válido."
    lat_cobertura = D(lat[0]["muestras_validas"])/mes
    jitter = muestras("jitter")
    n_jitter = sum(int(j["muestras_validas"]) for j in jitter)
    jitter_media = sum(D(j["valor"])*D(j["muestras_validas"]) for j in jitter)/D(n_jitter)
    # Contrato no fija una cadencia TWAMP; cobertura de jitter estimada condicional a 1 muestra/min.
    jitter_cobertura_condicional = D(n_jitter)/mes
    speed = muestras("throughput")
    media_speed = sum(D(m["valor"]) for m in speed)/D(len(speed)) if speed else None
    responden, tiempos_mttr = [], []
    for t in tickets:
        ap = datetime.fromisoformat(t["apertura"])
        r = datetime.fromisoformat(t["primera_respuesta"])
        fin = datetime.fromisoformat(t["fin_servicio"])
        respuesta = int((r-ap).total_seconds()/60)
        desde_ticket = int((fin-ap).total_seconds()/60)
        es_atribuible, desde_nms = estados[t["evento"]]
        responden.append({"ticket":t["ticket"],"evento":t["evento"],"respuesta_min":respuesta,
                          "restauracion_desde_ticket_min":desde_ticket,"cumple":respuesta<=60})
        if es_atribuible:
            tiempos_mttr.append({"ticket":t["ticket"],"restauracion_desde_nms_min":int(desde_nms),
                                 "restauracion_desde_ticket_min":desde_ticket})
    reglas = obj["objetivos"]
    # Evidencia insuficiente: la pérdida parcial de 18 días no permite conocer el mes completo.
    perdida_cobertura = D(18)/D(30)
    resultados = {
        "disponibilidad":{"objetivo":D(reglas["disponibilidad"]["valor"]),"medido":disponibilidad,"unidad":"%","veredicto":"NO CUMPLE" if disponibilidad<D(reglas["disponibilidad"]["valor"]) else "CUMPLE"},
        "latencia":{"objetivo":D(reglas["latencia"]["valor"]),"medido":D(lat[0]["valor"]),"unidad":"ms","cobertura":lat_cobertura,"veredicto":"CUMPLE" if lat_cobertura>=min_cobertura and D(lat[0]["valor"])<=D(reglas["latencia"]["valor"]) else "EVIDENCIA INSUFICIENTE" if lat_cobertura<min_cobertura else "NO CUMPLE"},
        "jitter":{"objetivo":D(reglas["jitter"]["valor"]),"medido":jitter_media,"unidad":"ms","muestras":n_jitter,"cobertura_condicional_60s":jitter_cobertura_condicional,"veredicto":"CUMPLE CON SALVEDAD" if jitter_media<=D(reglas["jitter"]["valor"]) else "NO CUMPLE CON SALVEDAD"},
        "perdida":{"objetivo":D(reglas["perdida"]["valor"]),"medido":None,"unidad":"%","medicion_parcial":D("0.31"),"cobertura":perdida_cobertura,"veredicto":"EVIDENCIA INSUFICIENTE"},
        "throughput":{"objetivo":D(reglas["throughput"]["valor"]),"medido":media_speed,"unidad":"Mbps","pruebas":len(speed),"veredicto": "EVIDENCIA INSUFICIENTE" if len(speed)<int(reglas["throughput"]["minimo_pruebas"]) else "CUMPLE" if media_speed>=D(reglas["throughput"]["valor"]) else "NO CUMPLE"},
        "respuesta":{"objetivo":D(reglas["respuesta"]["valor"]),"medido":D(max(t["respuesta_min"] for t in responden)),"unidad":"min","tickets":len(responden),"veredicto":"CUMPLE" if all(t["cumple"] for t in responden) else "NO CUMPLE"},
        "mttr":{"objetivo":D(reglas["mttr"]["valor"]),"medido":D(max(t["restauracion_desde_nms_min"] for t in tiempos_mttr)),"unidad":"min","tickets_atribuibles":len(tiempos_mttr),"veredicto":"CUMPLE" if all(t["restauracion_desde_nms_min"]<=D(reglas["mttr"]["valor"]) for t in tiempos_mttr) else "NO CUMPLE"}
    }
    credito_disponibilidad = D(0)
    if resultados["disponibilidad"]["veredicto"] == "NO CUMPLE":
        for tramo in obj["tramos_disponibilidad"]:
            if D(tramo["minimo"])<=disponibilidad<D(tramo["maximo_exclusivo"]):
                credito_disponibilidad=D(tramo["credito"])
                break
    # No se asignan créditos por métricas con evidencia insuficiente.
    otros = [m for m in ["latencia","jitter","perdida","throughput","respuesta"] if resultados[m]["veredicto"]=="NO CUMPLE"]
    credito_bruto=credito_disponibilidad+D(len(otros))*D(obj["credito_otros"])
    credito_aplicable=min(credito_bruto,D(obj["credito_maximo"]))
    A_cpe=D("0.9995"); A_fibra=D("0.9980"); A_pe=D("0.9999"); A_backbone=D("0.9999"); A_radio=D("0.9950")
    a_serie=A_cpe*A_fibra*A_pe*A_backbone
    a_acceso=1-(1-A_fibra)*(1-A_radio)
    a_respaldo=A_cpe*a_acceso*A_pe*A_backbone
    return {
        "periodo":obj["periodo"],"caso":"EVA 3 Agrícola Valle de Elqui - datos de enunciado",
        "eventos":lista_eventos,"tickets":responden,"restauraciones_atribuibles":tiempos_mttr,
        "minutos_mes":mes,"minutos_caida_fisica":total_fisico,"minutos_excluidos":total_fisico-total_atribuible,
        "minutos_caida_atribuible":total_atribuible,"minutos_permitidos":permitidos,
        "minutos_exceso":total_atribuible-permitidos,"resultados":resultados,
        "credito_disponibilidad":credito_disponibilidad,"credito_adicional_metricas":otros,
        "credito_total_fraccion":credito_aplicable,"credito_clp_neto":credito_aplicable*D(obj["cargo_mensual_neto_clp"]),
        "global":"NO CUMPLE" if any(r["veredicto"]=="NO CUMPLE" for r in resultados.values()) else "SIN INCUMPLIMIENTO DEMOSTRADO",
        "modelo_redundancia":{"serie":a_serie,"acceso_fibra_radio":a_acceso,"total_con_respaldo":a_respaldo,
                              "caida_serie_minutos_equivalentes":(1-a_serie)*mes,
                              "caida_respaldo_minutos_equivalentes":(1-a_respaldo)*mes,
                              "supuesto":"Independencia de fallas; CPE, PE y backbone comunes. Valores anuales usados como aproximación, no garantía mensual."},
        "limitaciones":["Pérdida: solo 18 de 30 días; no extrapolar 0,31%.",
                         "Jitter: comprobar que el colector fue independiente del que falló el 19-sep y validar cadencia/cobertura temporal.",
                         "La demarcación no demuestra por sí misma throughput simétrico en ambas direcciones.",
                         "El extracto contractual no define inicio de MTTR; se evalúa conservadoramente desde caída NMS."]
    }


def serializable(x):
    if isinstance(x,Decimal): return float(x)
    if isinstance(x,dict): return {k:serializable(v) for k,v in x.items()}
    if isinstance(x,list): return [serializable(v) for v in x]
    return x


def mostrar(resultado):
    print("EVA 3 | VALIDACIÓN SLA | SEPTIEMBRE 2026")
    print("Datos: anexos docentes, no mediciones independientes")
    print("-"*70)
    print(f"Caída física: {resultado['minutos_caida_fisica']} min | Excluida: {resultado['minutos_excluidos']} min | Atribuible: {resultado['minutos_caida_atribuible']} min")
    print(f"Presupuesto de caída: {resultado['minutos_permitidos']:.2f} min | Exceso: {resultado['minutos_exceso']:.2f} min")
    print(f"{'MÉTRICA':<17}{'MEDIDO':<23}VEREDICTO")
    for name, row in resultado["resultados"].items():
        med = "no determinable" if row["medido"] is None else f"{row['medido']:.5f} {row['unidad']}"
        print(f"{name:<17}{med:<23}{row['veredicto']}")
    print("-"*70)
    print(f"GLOBAL: {resultado['global']}")
    print(f"CRÉDITO: {resultado['credito_total_fraccion']*100:.2f}% = ${resultado['credito_clp_neto']:,.0f} CLP netos")
    print("ADVERTENCIA: jitter condicionado; pérdida insuficiente (60% de días).")
    print("PROYECCIÓN SERIE: {:.6f}% | ACCESO CON RADIO: {:.6f}%".format(resultado['modelo_redundancia']['serie']*100,resultado['modelo_redundancia']['total_con_respaldo']*100))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--objetivos", "-o", required=True, type=Path)
    p.add_argument("--datos", "-d", required=True, type=Path)
    p.add_argument("--salida-json", type=Path)
    p.add_argument("--salida-texto", type=Path)
    args=p.parse_args()
    with open(args.objetivos,encoding="utf8") as f: obj=yaml.safe_load(f)
    res=evaluar(obj,cargar_csv(args.datos/"eventos.csv"),cargar_csv(args.datos/"tickets.csv"),cargar_csv(args.datos/"mediciones.csv"))
    if args.salida_json:
        args.salida_json.parent.mkdir(parents=True,exist_ok=True)
        args.salida_json.write_text(json.dumps(serializable(res),ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    from io import StringIO
    import contextlib
    buf=StringIO()
    with contextlib.redirect_stdout(buf): mostrar(res)
    s=buf.getvalue()
    if args.salida_texto:
        args.salida_texto.parent.mkdir(parents=True,exist_ok=True)
        args.salida_texto.write_text(s,encoding="utf8")
    print(s,end="")

if __name__=="__main__": main()
