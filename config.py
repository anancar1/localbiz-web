"""localbiz-web — Pipeline to find local businesses without websites and
generate landing pages for them."""

# Target market
CITY = "Xàtiva"
REGION = "Valencia"
COUNTRY = "España"

# Categories to search on Google Maps
CATEGORIES = [
    "restaurante",
    "peluqueria",
    "fontanero",
    "electricista",
    "mecanico coches",
    "tienda ropa",
    "farmacia",
    "bar cafeteria",
    "dentista",
    "gimnasio",
]

# Output paths
DATA_DIR = "output/data"
HTML_DIR = "output/html"

# Playwright settings
HEADLESS = True
VIEWPORT = {"width": 1280, "height": 900}
TIMEOUT = 30000  # 30s

# Checker settings
WEBSITE_TIMEOUT = 10  # seconds
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
