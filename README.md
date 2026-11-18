# EVA 3: auditoría del SLA de Agrícola Valle de Elqui

**Proyecto académico independiente para la cuenta de GitHub `MTAINDARY`.**

Evalúa el enlace simétrico de Internet dedicado de 200 Mbps en Vicuña durante septiembre de 2026 con los datos **del enunciado docente**, sin inventar mediciones. Está desarrollado con una calculadora Python propia, los datos fuente en CSV, el contrato en YAML, pruebas unitarias, una carpeta de evidencias y un informe técnico completo.

## 1. Estructura

```text
EVA3_SLA_MTAINDARY/
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── .gitignore
├── herramientas/
│   ├── calc_sla.py
│   └── objetivos.yaml
├── datos/
│   ├── eventos.csv
│   ├── tickets.csv
│   └── mediciones.csv
├── tests/
│   └── test_calc_sla.py
├── evidencias/
│   ├── salida_calc_sla.txt
│   ├── resultados.json
│   ├── pruebas_unitarias.txt
│   ├── disponibilidad.png
│   ├── jitter.png
│   └── integridad_archivos.sha256
└── docs/
    ├── informe_eva3.md
    ├── guia_evidencias.md
    └── referencias.md
```

## 2. Ejecución en Windows / PowerShell

Requisitos: Python 3.10 o superior, `git` y conexión a GitHub para publicar. Desde la raíz:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python herramientas/calc_sla.py -o herramientas/objetivos.yaml -d datos --salida-json evidencias/resultados.json --salida-texto evidencias/salida_calc_sla.txt
python -m unittest discover -s tests -v 2>&1 | Tee-Object -FilePath evidencias/pruebas_unitarias_windows.txt
```

Si PowerShell impide activar el entorno, utiliza directamente `.\.venv\Scripts\python.exe` en los comandos en lugar de activar la sesión. La salida de Windows es **tu evidencia local adicional**, distinta de la ejecución incluida en el paquete.

## 3. Qué prueba la calculadora

- Correlaciona cinco eventos y cuatro tickets y calcula sus duraciones desde marcas temporales.
- Aplica las exclusiones por mantención avisada y responsabilidad de energía del cliente.
- Calcula disponibilidad, caída permitida y exceso sobre 43.200 min.
- Calcula jitter como promedio **ponderado por cantidad de muestras**, no promedio simple de semanas.
- Desestima pruebas fuera de la demarcación y el Speedtest por Wi-Fi.
- Informa **evidencia insuficiente** para la pérdida de paquetes por cobertura del 60%.
- Compara el tiempo de respuesta individual de los cuatro tickets y MTTR de tres incidentes atribuibles.
- Calcula el crédito aplicando los tramos y el tope contractual.
- Modela la disponibilidad en serie y una alternativa con fibra y radio en paralelo, con elementos comunes.

**Resultado:** incumple disponibilidad (99,62963%) y respuesta (66 min); crédito de 15%, equivalente a **$180.000 netos**. Otros resultados y salvedades constan en `docs/informe_eva3.md`.

## 4. Pruebas y evidencias

La primera ejecución y **11 pruebas automatizadas** se ejecutaron en el entorno de preparación y se guardan bajo `evidencias/`. Para la entrega, repite los comandos en tu PC y captura la terminal, `git status`, el registro de commits y el tag. La guía de pantallazos está en `docs/guia_evidencias.md`. Los PNG son gráficos generados con los datos de los anexos, no supuestas capturas de Zabbix o iperf3.

## 5. Publicación en tu GitHub

La cuenta conectada verificada es **MTAINDARY**. La creación remota debe realizarse en esa cuenta porque el acceso disponible en este chat no incluye crear repositorios nuevos. No publiques en el repositorio del compañero.

1. Ve a <https://github.com/new>, confirma que el propietario sea `MTAINDARY` y crea un repositorio público vacío llamado `eva3-sla-valle-elqui` (sin README ni .gitignore inicial).
2. Abre PowerShell dentro de esta carpeta y ejecuta:

```powershell
git init
git branch -M main
git add .
git commit -m "feat: desarrolla auditoria SLA Valle de Elqui"
git remote add origin https://github.com/MTAINDARY/eva3-sla-valle-elqui.git
git push -u origin main
git tag -a v1.1 -m "EVA3: evidencia y auditoria SLA"
git push origin v1.1
```

**Enlace que obtendrás después de crearlo:** `https://github.com/MTAINDARY/eva3-sla-valle-elqui`. El enlace no se considera publicado hasta verificar que GitHub muestre el repositorio, los archivos y el tag.

Si Git exige configurar autor, usa `git config --global user.name "TU NOMBRE"` y `git config --global user.email "TU EMAIL CONFIGURADO EN GITHUB"` con tus datos propios. No uses los datos de otro integrante.

## 6. Fuentes

EVA 3 CASO DE ESTUDIO.pdf, pp. 1–6; material docente SLA y niveles de servicio; Caso_Clinica_Limari.pdf usado solo como pauta de estructura, **no como fuente de resultados**. Toda cifra del informe proviene de los anexos 1–7 del caso Valle de Elqui.
