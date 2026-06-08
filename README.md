# localbiz-web 🏗️

Pipeline automatizado para encontrar negocios locales sin pagina web en Xativa (Valencia, España) y generarles landing pages profesionales.

## Como funciona

```
Discovery → Checker → Gatherer → Generator → Deploy
   🔍          🎯        📸          🌐         🚀
```

1. **Discovery** — Busca negocios en Google Maps por categoria
2. **Checker** — Detecta que negocios no tienen pagina web
3. **Gatherer** — Extrae fotos, telefono, horarios y mas datos
4. **Generator** — Crea HTML profesional con DESIGN.md + Jinja2
5. **Deploy** — Sube a Vercel (gratis, SSL, dominio .vercel.app)

## Uso rapido

```bash
# Instalar dependencias
pip install -r requirements.txt
python -m playwright install chromium

# Demo (3 paginas de ejemplo, sin Google Maps)
python pipeline.py demo

# Deploy a Vercel
export VERCEL_TOKEN=tu_token
python pipeline.py deploy

# Pipeline completo
python pipeline.py discover
python pipeline.py check
python pipeline.py gather
python pipeline.py generate
python pipeline.py deploy
```

## Despliegue en Vercel

El deploy es **gratuito** (plan Hobby de Vercel):
- Ancho de banda ilimitado para estaticos
- SSL automatico
- Dominio `*.vercel.app` gratis

Necesitas un token de Vercel: https://vercel.com/account/tokens

```bash
export VERCEL_TOKEN=vcp_xxxxx
python pipeline.py deploy
```

La pagina indice lista todos los negocios en `https://[proyecto].vercel.app/`

## Mercado

- **68-70%** de las micro-pymes espanolas no tienen web (~1.2M negocios)
- Solo en Xativa: **540-820** negocios sin web
- Mercado potencial: **160K – 410K euros**

## Estructura

```
localbiz-web/
├── pipeline.py          # Orquestador principal
├── config.py            # Configuracion
├── DESIGN.md            # Design tokens
├── discovery/           # Google Maps scraper
├── checker/             # Detector de presencia web
├── gatherer/            # Extractor de datos
├── generator/           # Generador HTML (Jinja2)
│   └── templates/
├── deploy/              # Deploy a Vercel
└── output/
    ├── data/            # JSON con datos
    └── html/            # Paginas generadas
```

## Tech stack

- Python 3.11+ · Playwright · Jinja2 · DESIGN.md
- Google Maps scraping (sin API key)
- CSS moderno con custom properties
- Vercel (hosting gratuito)
