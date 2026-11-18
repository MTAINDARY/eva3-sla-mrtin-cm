
# Caso práctico: Agrícola Valle de Elqui SpA

## 1. Descripción del caso

Este ejemplo corresponde a la Evaluación Sumativa 3 de Infraestructura de Telecomunicaciones Avanzada.

Se analiza el cumplimiento del Acuerdo de Nivel de Servicio (SLA) de un enlace dedicado de Internet simétrico de 200 Mbps, contratado por Agrícola Valle de Elqui SpA con NorteNet Telecomunicaciones.

El período evaluado comprende del 1 al 30 de septiembre de 2026.

## 2. Objetivo

Verificar el cumplimiento contractual de los indicadores de disponibilidad, latencia, jitter, pérdida de paquetes, throughput, tiempo de primera respuesta y MTTR.

También se determina el crédito económico correspondiente a los incumplimientos acreditados.

## 3. Archivos utilizados

Los archivos se encuentran en las carpetas principales del repositorio para evitar duplicar información.

### Datos del caso
- [Eventos de interrupción](../../datos/eventos.csv)
- [Tickets de incidentes](../../datos/tickets.csv)
- [Mediciones de red](../../datos/mediciones.csv)

### Herramientas
- [Calculadora SLA en Python](../../herramientas/calc_sla.py)
- [Parámetros contractuales YAML](../../herramientas/objetivos.yaml)
- [Pruebas automatizadas](../../tests/test_calc_sla.py)

### Resultados y documentación
- [Resultados JSON](../../evidencias/resultados.json)
- [Salida de la calculadora](../../evidencias/salida_calc_sla.txt)
- [Informe técnico](../../docs/informe_eva3.md)
- [Guía de evidencias](../../docs/guia_evidencias.md)

## 4. Resultados obtenidos

| Indicador | Resultado | Veredicto |
|---|---|---|
| Disponibilidad | 99,62963 % | No cumple |
| Latencia | 27,4 ms | Cumple |
| Jitter | 9,91945 ms | Cumple con salvedad |
| Pérdida de paquetes | Cobertura del 60 % | Evidencia insuficiente |
| Throughput | 180,75 Mbps | Cumple |
| Primera respuesta | 66 min máximo | No cumple |
| MTTR | 75 min máximo | Cumple |

El servicio presenta incumplimientos de disponibilidad y tiempo de primera respuesta.

Crédito contractual acreditado: **15 % del cargo mensual, equivalente a $180.000 CLP netos**.

## 5. Ejecución del ejemplo

Desde la raíz del repositorio:

```powershell
py -m pip install -r requirements.txt
py herramientas/calc_sla.py -o herramientas/objetivos.yaml -d datos
py -m unittest discover -s tests -v
```

La calculadora procesa los registros del caso docente y genera los resultados de la auditoría.

## 6. Alcance y limitaciones

Los datos corresponden a los anexos proporcionados para la evaluación académica. No representan mediciones independientes realizadas sobre la infraestructura real del proveedor.

La pérdida de paquetes no dispone de cobertura mensual suficiente. El resultado de jitter requiere confirmar la procedencia y validez de las muestras posteriores al 19 de septiembre.

## 7. Repositorio principal

[MTAINDARY/eva3-sla-mrtin-cm](https://github.com/MTAINDARY/eva3-sla-mrtin-cm)
