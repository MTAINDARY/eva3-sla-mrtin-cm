# Guía de evidencias prácticas - EVA3

Esta guía diferencia **evidencias reproducibles** (resultado de ejecutar la calculadora) de **datos fuente del caso** (registros transcritos desde el PDF). No se debe presentar una tabla del enunciado como captura directa del equipo del proveedor.

## Preparación de la PC

1. Instala Python 3.10+ y Git; revisa con `python --version` y `git --version`.
2. Descomprime el proyecto, abre su carpeta con VS Code y abre una terminal PowerShell.
3. Ejecuta los comandos de instalación y prueba indicados en `README.md`.

## Evidencias para capturar y adjuntar al informe

- **E01 - Estructura del proyecto:** captura VS Code con `herramientas/`, `datos/`, `tests/`, `evidencias/`, `docs/`, `README.md` y `CHANGELOG.md` visibles.
- **E02 - Objetivos:** captura `herramientas/objetivos.yaml`, mostrando los umbrales y la cláusula de créditos.
- **E03 - Datos válidos y descartados:** captura `datos/mediciones.csv`; resalta `si`, `no`, `parcial`, y demuestra que el Speedtest Wi-Fi y PE-core se excluyen.
- **E04 - Ejecución de la calculadora:** ejecuta `python herramientas/calc_sla.py -o herramientas/objetivos.yaml -d datos --salida-json evidencias/resultados.json --salida-texto evidencias/salida_calc_sla.txt` y captura la consola con 99,62963%, 66 min, 15%, $180.000.
- **E05 - Pruebas automatizadas:** ejecuta `python -m unittest discover -s tests -v`; captura que se ejecutaron 11 tests y el resultado `OK`.
- **E06 - Resultado JSON:** captura `evidencias/resultados.json` y señala `EVIDENCIA INSUFICIENTE` de pérdida.
- **E07 - Git local:** después de hacer commit, ejecuta `git log --oneline -3` y `git status`; captura que hay un commit y el árbol limpio.
- **E08 - Publicación:** desde tu navegador, entra al repositorio público que creaste bajo `MTAINDARY`, captura la URL, el contenido y la pestaña de etiquetas (tag v1.1).
- **E09 - Validación de etiqueta:** ejecuta `git show --stat v1.1`, guarda la salida y captura el commit al que apunta.

## Integridad

El archivo `evidencias/integridad_archivos.sha256` registra las sumas SHA-256 del código, CSV, YAML y resultados generados. Se trata de una comprobación local, no de una firma electrónica ni de un sello temporal externo.

## Lo que falta validar fuera del enunciado

- El docente debe confirmar si el bloque de jitter del 22 al 30 de septiembre proviene de un TWAMP distinto del colector detenido el 19.
- No existen contadores mensuales válidos para pérdida posteriores al 18 de septiembre. No inventar valores.
- No se aportan registros crudos de `iperf3` ni Zabbix. Por ello, las capturas que generes deben mostrar ejecución del cálculo del caso, no una medición de red inexistente.

## Repositorio remoto

No agregues el enlace definitivo al informe hasta que exista y hayas comprobado el tag `v1.1`. Se sugiere `MTAINDARY/eva3-sla-valle-elqui`, pero es solo una ubicación propuesta hasta su creación.
