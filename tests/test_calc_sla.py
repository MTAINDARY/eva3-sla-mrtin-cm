"""Pruebas originales: verifican cálculo, exclusiones, cobertura y crédito."""
import sys
import unittest
import copy
from pathlib import Path
from decimal import Decimal
import yaml
RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/"herramientas"))
from calc_sla import cargar_csv, evaluar, D

class TestEVA3(unittest.TestCase):
    def setUp(self):
        self.obj=yaml.safe_load((RAIZ/"herramientas/objetivos.yaml").read_text(encoding="utf8"))
        self.ev=cargar_csv(RAIZ/"datos/eventos.csv")
        self.tk=cargar_csv(RAIZ/"datos/tickets.csv")
        self.me=cargar_csv(RAIZ/"datos/mediciones.csv")
        self.r=evaluar(self.obj,self.ev,self.tk,self.me)

    def test_minutos_por_evento(self):
        self.assertEqual([e["minutos"] for e in self.r["eventos"]],[210,55,105,75,30])
        self.assertEqual(self.r["minutos_caida_fisica"],D(475))
        self.assertEqual(self.r["minutos_excluidos"],D(315))
        self.assertEqual(self.r["minutos_caida_atribuible"],D(160))

    def test_disponibilidad_y_exceso(self):
        self.assertAlmostEqual(float(self.r["resultados"]["disponibilidad"]["medido"]),99.6296296296,8)
        self.assertEqual(self.r["minutos_permitidos"],D('43.2'))
        self.assertEqual(self.r["minutos_exceso"],D('116.8'))

    def test_latencia_y_cobertura(self):
        self.assertEqual(self.r["resultados"]["latencia"]["veredicto"],"CUMPLE")
        self.assertGreater(self.r["resultados"]["latencia"]["cobertura"],D('0.9'))

    def test_jitter_ponderado_no_simple(self):
        self.assertAlmostEqual(float(self.r["resultados"]["jitter"]["medido"]),423808.5/42725,10)
        self.assertEqual(self.r["resultados"]["jitter"]["veredicto"],"CUMPLE CON SALVEDAD")

    def test_perdida_no_extrapolada(self):
        self.assertIsNone(self.r["resultados"]["perdida"]["medido"])
        self.assertEqual(self.r["resultados"]["perdida"]["veredicto"],"EVIDENCIA INSUFICIENTE")

    def test_speedtest_no_incluido(self):
        self.assertEqual(self.r["resultados"]["throughput"]["pruebas"],4)
        self.assertEqual(self.r["resultados"]["throughput"]["medido"],D('180.75'))

    def test_respuesta_66_vs_mttr_75(self):
        self.assertEqual(self.r["resultados"]["respuesta"]["medido"],D(66))
        self.assertEqual(self.r["resultados"]["mttr"]["medido"],D(75))
        self.assertEqual(self.r["resultados"]["respuesta"]["veredicto"],"NO CUMPLE")

    def test_credito_15(self):
        self.assertEqual(self.r["credito_total_fraccion"],D('0.15'))
        self.assertEqual(self.r["credito_clp_neto"],D(180000))

    def test_credito_si_todos_responden_en_60(self):
        tk=copy.deepcopy(self.tk)
        for x in tk:
            if x['ticket']=='INC-2672':x['primera_respuesta']='2026-09-21T23:09'
        r=evaluar(self.obj,self.ev,tk,self.me)
        self.assertEqual(r['credito_clp_neto'],D(120000))

    def test_regla_menos_de_cuatro_pruebas(self):
        me=[x for x in self.me if not(x['metrica']=='throughput' and x['fecha_o_bloque']=='2026-09-26')]
        r=evaluar(self.obj,self.ev,self.tk,me)
        self.assertEqual(r['resultados']['throughput']['veredicto'],'EVIDENCIA INSUFICIENTE')

    def test_modelo_radio_no_confundir_con_sistema_completo(self):
        self.assertLess(self.r['modelo_redundancia']['serie'],D('0.999'))
        self.assertGreater(self.r['modelo_redundancia']['total_con_respaldo'],D('0.999'))

if __name__=='__main__': unittest.main(verbosity=2)
