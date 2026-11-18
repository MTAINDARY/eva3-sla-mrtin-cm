
# EVA 3 — Verificación del cumplimiento de SLA
## Caso de estudio: Agrícola Valle de Elqui SpA

**Institución:** INACAP La Serena  
**Carrera:** Ingeniería en Telecomunicaciones  
**Asignatura:** Infraestructura de Telecomunicaciones Avanzada  
**Estudiante:** Martín Cortés Molina  
**Profesor:** Daniel Ruz Moreno  
**Evaluación:** Sumativa 3  
**Período analizado:** Septiembre de 2026  

**Repositorio oficial:**  
https://github.com/MTAINDARY/eva3-sla-mrtin-cm

---

## 1. Descripción del proyecto

Este repositorio contiene el desarrollo práctico de la Evaluación Sumativa 3, cuyo objetivo es verificar el cumplimiento del Acuerdo de Nivel de Servicio (SLA) entre Agrícola Valle de Elqui SpA y NorteNet Telecomunicaciones.

El caso corresponde a un enlace de Internet dedicado simétrico de 200 Mbps instalado en la planta de Vicuña, utilizado para servicios empresariales como ERP, trazabilidad de exportaciones y telefonía IP.

El análisis considera las interrupciones, mediciones de rendimiento y registros de incidentes correspondientes a septiembre de 2026.

Los datos utilizados provienen de los anexos docentes de la evaluación. No corresponden a mediciones independientes sobre una red de producción.

## 2. Objetivos

- Identificar los compromisos establecidos en el contrato SLA.
- Clasificar los eventos de interrupción según su responsabilidad contractual.
- Calcular la disponibilidad mensual y el tiempo de caída atribuible.
- Evaluar latencia, jitter, pérdida de paquetes y throughput.
- Verificar los tiempos de primera respuesta y restauración (MTTR).
- Determinar los créditos económicos por incumplimientos demostrados.
- Analizar la disponibilidad de la infraestructura y posibles alternativas de redundancia.
- Automatizar los cálculos mediante Python.
- Documentar los resultados y evidencias utilizando Git y GitHub.

## 3. Estructura del repositorio

```text
EVA3_SLA_MTAINDARY/
|
|-- README.md
|-- CHANGELOG.md
|-- requirements.txt
|-- .gitignore
|
|-- datos/
|   |-- eventos.csv
|   |-- tickets.csv
|   `-- mediciones.csv
|
|-- herramientas/
|   |-- calc_sla.py
|   `-- objetivos.yaml
|
|-- tests/
|   `-- test_calc_sla.py
|
|-- evidencias/
|   |-- resultados.json
|   |-- salida_calc_sla.txt
|   |-- pruebas_unitarias.txt
|   |-- disponibilidad.png
|   |-- jitter.png
|   `-- integridad_archivos.sha256
|
|-- docs/
|   |-- informe_eva3.md
|   |-- guia_evidencias.md
|   `-- referencias.md
|
`-- ejemplos/
    `-- caso-valle-elqui/
        `-- README.md
```

### Descripción de los componentes

| Directorio | Función |
|---|---|
| `datos/` | Registros de eventos, tickets y mediciones del caso. |
| `herramientas/` | Calculadora Python y parámetros contractuales YAML. |
| `tests/` | Pruebas automatizadas del programa. |
| `evidencias/` | Resultados, gráficos y registros de ejecución. |
| `docs/` | Informe técnico, referencias y guía de evidencias. |
| `ejemplos/caso-valle-elqui/` | Documentación específica del caso con enlaces a los archivos utilizados. |

### Acceso directo al caso práctico

[Ver caso Agrícola Valle de Elqui](ejemplos/caso-valle-elqui/README.md)

## 4. Metodología de evaluación

El procedimiento de auditoría comprende cinco etapas:

**Etapa 1 — Revisión contractual**

Se identifican los objetivos de disponibilidad, calidad de servicio y tiempos de atención establecidos en el SLA.

**Etapa 2 — Preparación de datos**

Se organizan los eventos, mediciones y tickets en archivos CSV. Los umbrales y las reglas de crédito se almacenan en `objetivos.yaml`.

**Etapa 3 — Procesamiento**

La calculadora `calc_sla.py` interpreta los registros, aplica las exclusiones y calcula las métricas contractuales.

**Etapa 4 — Validación**

Se ejecutan pruebas unitarias para comprobar los cálculos de disponibilidad, jitter, throughput, tiempos de respuesta, créditos y redundancia.

**Etapa 5 — Documentación**

Se generan resultados JSON, salidas de consola, gráficos e informes. La publicación en GitHub permite consultar el código y su historial.

## 5. Requisitos de ejecución

Para ejecutar el proyecto se necesita:

- Python 3.10 o superior.
- Git para el control de versiones.
- Visual Studio Code o cualquier editor compatible con Python.
- Dependencias definidas en `requirements.txt`.

### Instalación

Abrir PowerShell desde la carpeta principal del proyecto.

Instalar las dependencias:

```powershell
py -m pip install -r requirements.txt
```

### Ejecutar la calculadora

```powershell
py herramientas/calc_sla.py -o herramientas/objetivos.yaml -d datos --salida-json evidencias/resultados.json --salida-texto evidencias/salida_calc_sla.txt
```

La calculadora procesa los registros del caso y muestra el veredicto de las métricas junto con el crédito contractual aplicable.

### Ejecutar las pruebas automatizadas

```powershell
py -m unittest discover -s tests -v
```

En la ejecución documentada se completaron correctamente 11 pruebas automatizadas.

Resultado registrado:

```text
Ran 11 tests

OK
```

## 6. Resultados obtenidos

| Métrica | Objetivo SLA | Resultado | Veredicto |
|---|---|---|---|
| Disponibilidad | >= 99,9 % | 99,62963 % | NO CUMPLE |
| Latencia RTT | <= 30 ms | 27,4 ms | CUMPLE |
| Jitter | <= 10 ms | 9,91945 ms | CUMPLE CON SALVEDAD |
| Pérdida | <= 0,5 % | Cobertura del 60 % | EVIDENCIA INSUFICIENTE |
| Throughput | >= 180 Mbps | 180,75 Mbps | CUMPLE |
| Primera respuesta | <= 60 min | 66 min máximo | NO CUMPLE |
| MTTR | <= 240 min | 75 min máximo | CUMPLE |

### Disponibilidad contractual

Tiempo total evaluado: 43.200 minutos.

Interrupciones físicas: 475 minutos.

Interrupciones excluidas: 315 minutos.

Interrupciones atribuibles al proveedor: 160 minutos.

```text
Disponibilidad = (43.200 - 160) / 43.200 x 100

Disponibilidad = 99,62963 %
```

El servicio no alcanza el mínimo contractual del 99,9 %.

### Crédito de servicio

El incumplimiento de disponibilidad genera un crédito del 10 %.

El incumplimiento del tiempo de primera respuesta genera un crédito adicional del 5 %.

```text
Credito total = 10 % + 5 % = 15 %

Credito neto = $1.200.000 x 0,15

Credito neto = $180.000 CLP
```

**Veredicto global: NO CUMPLE SLA.**

**Crédito contractual acreditado: $180.000 CLP netos.**

## 7. Análisis de redundancia

Se evaluaron dos alternativas utilizando las disponibilidades por componente proporcionadas en el caso.

| Arquitectura | Disponibilidad teórica |
|---|---|
| Acceso actual con fibra única | 99,730151 % |
| Fibra con radioenlace de respaldo | 99,929012 % |
| Objetivo contractual | 99,9 % |

El modelo indica que el acceso único no alcanza la disponibilidad objetivo, mientras que la alternativa con radioenlace podría superarla bajo determinados supuestos.

El cálculo supone independencia de fallas entre fibra y radio, conmutación funcional y disponibilidad de los componentes comunes.

Estos resultados son proyecciones de diseño y no constituyen garantías mensuales ni mediciones reales.

## 8. Evidencias de ejecución

Los resultados procesados se encuentran en los siguientes archivos:

- [Resultados JSON](evidencias/resultados.json)
- [Salida de la calculadora](evidencias/salida_calc_sla.txt)
- [Pruebas automatizadas](evidencias/pruebas_unitarias.txt)
- [Gráfico de disponibilidad](evidencias/disponibilidad.png)
- [Gráfico de jitter](evidencias/jitter.png)
- [Guía de evidencias](docs/guia_evidencias.md)
- [Informe técnico en Markdown](docs/informe_eva3.md)

Las capturas de PowerShell, Visual Studio Code y GitHub se incorporaron al informe PDF de evaluación.

La calculadora utiliza los datos del enunciado y no sustituye una herramienta de medición de red.

## 9. Control de versiones y GitHub

**Propietario:** MTAINDARY

**Repositorio:**  
https://github.com/MTAINDARY/eva3-sla-mrtin-cm

**Rama principal:** `main`

**Etiqueta original:** `v1.1`

**Commit de la versión v1.1:** `0956b12`

La rama `main` contiene la documentación adicional del caso práctico en `ejemplos/caso-valle-elqui/`.

La etiqueta `v1.1` corresponde a la primera versión publicada del toolkit y se conserva como referencia de esa entrega. No incluye la carpeta de ejemplo añadida posteriormente.

### Enlaces

- [Repositorio principal](https://github.com/MTAINDARY/eva3-sla-mrtin-cm)
- [Caso práctico en main](https://github.com/MTAINDARY/eva3-sla-mrtin-cm/tree/main/ejemplos/caso-valle-elqui)
- [Versión v1.1](https://github.com/MTAINDARY/eva3-sla-mrtin-cm/tree/v1.1)
- [Historial de cambios](CHANGELOG.md)

## 10. Limitaciones del análisis

- Las mediciones provienen de los anexos de la evaluación.
- La pérdida de paquetes solo tiene cobertura del 60 % del mes y no permite emitir un veredicto mensual.
- El cumplimiento de jitter queda sujeto a verificar la procedencia de las muestras posteriores al 19 de septiembre.
- Las pruebas de throughput no permiten comprobar de forma independiente ambas direcciones del enlace.
- El contrato resumido no define de manera inequívoca el instante inicial del MTTR.
- Los modelos de redundancia dependen de supuestos de independencia y disponibilidad de componentes.

Estas limitaciones se documentan para evitar conclusiones que no estén respaldadas por las evidencias disponibles.

## 11. Conclusión

La auditoría permitió determinar que NorteNet Telecomunicaciones incumplió el SLA correspondiente a septiembre de 2026, principalmente por disponibilidad y tiempo de primera respuesta.

Se acreditó un crédito contractual del 15 %, equivalente a $180.000 CLP netos.

El desarrollo incluye una calculadora Python, parámetros YAML, registros CSV, once pruebas automatizadas, resultados reproducibles y documentación técnica versionada en GitHub.

El proyecto permite demostrar la aplicación práctica de herramientas informáticas en la verificación y análisis de acuerdos de nivel de servicio en redes de telecomunicaciones.

## 12. Referencias

- INACAP (2026). *EVA 3 CASO DE ESTUDIO*. Material de evaluación.
- INACAP. *SLA y niveles de servicio en redes*. Material docente.
- INACAP. *SLA y niveles de servicio: conceptos clave*. Material docente.
- IETF. [RFC 3393 — IP Packet Delay Variation Metric](https://www.rfc-editor.org/rfc/rfc3393).
- IETF. [RFC 5357 — A Two-Way Active Measurement Protocol](https://www.rfc-editor.org/rfc/rfc5357).
- IETF. [RFC 6349 — Framework for TCP Throughput Testing](https://www.rfc-editor.org/rfc/rfc6349).

Para más información, consultar [docs/referencias.md](docs/referencias.md).
