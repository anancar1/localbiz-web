"""LLM Content module — generates Spanish descriptions for businesses.

Uses the configured LLM provider to create compelling, localised
descriptions in Spanish for each business based on its category,
location, and type.
"""

import json
from pathlib import Path
from typing import Optional

import config


# Fallback templates by category — used when LLM is unavailable
DESCRIPTION_TEMPLATES = {
    "restaurante": "Cocina tradicional {category_type} en pleno centro de {city}. "
                   "Productos frescos de temporada y recetas de la comarca. "
                   "Ambiente acogedor y servicio cercano. Ven a conocernos.",
    "bar cafeteria": "El mejor cafe y desayunos de {city}. Tapas, bocadillos y "
                     "ambiente de barrio. Terraza exterior y zona interior climatizada. "
                     "¡Te esperamos!",
    "peluqueria": "Tu peluqueria de confianza en {city}. Cortes de ultimas tendencias, "
                  "coloracion, mechas y tratamientos capilares. Productos profesionales "
                  "y atencion personalizada. Pide cita sin compromiso.",
    "fontanero": "Servicios de fontaneria profesional en {city} y comarca. Averias, "
                 "instalaciones, calderas, calefaccion y fontaneria general. "
                 "Presupuesto sin compromiso. Urgencias 24h.",
    "electricista": "Electricista profesional en {city}. Instalaciones nuevas, reformas, "
                    "averias, boletines electricos (CIE) y certificados energeticos. "
                    "Servicio rapido y presupuesto sin compromiso.",
    "mecanico coches": "Taller mecanico de confianza en {city}. Reparacion y mantenimiento "
                       "de todas las marcas. Diagnosis computerizada, cambios de aceite, "
                       "frenos, climatizacion y mucho mas.",
    "tienda ropa": "Moda y complementos en {city}. Ultimas tendencias para hombre, mujer "
                   "y nino. Ropa de temporada, accesorios y atencion personalizada. "
                   "Visitanos sin compromiso.",
    "farmacia": "Farmacia en {city}. Medicamentos, productos de parafarmacia, dermocosmetica "
                "y atencion farmaceutica personalizada. Tu salud es lo primero.",
    "dentista": "Clinica dental en {city}. Odontologia general, ortodoncia, implantes, "
                "estetica dental y urgencias. Tecnologia avanzada y trato cercano. "
                "Primera consulta gratuita.",
    "gimnasio": "Tu gimnasio en {city}. Sala fitness, clases dirigidas, entrenamiento "
                "personal y zona de peso libre. Ambiente motivador y monitores titulados. "
                "¡Prueba una clase gratis!",
}


def generate_description(business: dict) -> str:
    """Generate a Spanish description for a business.

    Uses template-based generation. For full LLM generation,
    set LLM_API_KEY in .env and uncomment the API path.
    """
    name = business.get("name", "")
    category = business.get("category", "negocio")
    biz_type = business.get("type", category)
    city = business.get("address", "").split(",")[0] if business.get("address") else config.CITY

    # Try to use the template for this category
    template = DESCRIPTION_TEMPLATES.get(category)
    if template:
        return template.format(city=config.CITY, category=biz_type, category_type=biz_type)

    # Generic fallback
    return (
        f"{name} es tu {biz_type} de confianza en {config.CITY}. "
        f"Profesionalidad, experiencia y trato cercano. "
        f"Contacta sin compromiso y cuentanos que necesitas."
    )


def enrich(businesses: list[dict] = None) -> list[dict]:
    """Add LLM-generated descriptions to businesses that lack them."""
    if businesses is None:
        gathered_path = Path(config.DATA_DIR) / "gathered.json"
        if not gathered_path.exists():
            # Try checked.json
            checked_path = Path(config.DATA_DIR) / "checked.json"
            if not checked_path.exists():
                print("No data found. Run pipeline first.")
                return []
            businesses = json.loads(checked_path.read_text(encoding="utf-8"))
        else:
            businesses = json.loads(gathered_path.read_text(encoding="utf-8"))

    no_web = [b for b in businesses if not b.get("has_website", False)]
    total = len(no_web)

    print(f"\nGenerating descriptions for {total} businesses...\n")

    enriched_count = 0
    for biz in no_web:
        if not biz.get("description"):
            biz["description"] = generate_description(biz)
            enriched_count += 1
            print(f"  {biz['name']}: generated")

    print(f"\nDone: {enriched_count} descriptions generated")

    # Save
    output_path = Path(config.DATA_DIR) / "gathered.json"
    output_path.write_text(json.dumps(businesses, indent=2, ensure_ascii=False), encoding="utf-8")
    return businesses
