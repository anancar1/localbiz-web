#!/usr/bin/env python3
"""localbiz-web — Pipeline principal."""

import sys, json
from pathlib import Path
import config


def run_discovery():
    from discovery import discover
    return discover()


def run_checker():
    from checker import check
    data_path = Path(config.DATA_DIR) / "discovered.json"
    if not data_path.exists():
        print("No data. Run: python pipeline.py discover")
        return []
    return check(json.loads(data_path.read_text(encoding="utf-8")))


def run_gatherer():
    from gatherer import gather
    data_path = Path(config.DATA_DIR) / "checked.json"
    if not data_path.exists():
        print("No data. Run: python pipeline.py check")
        return []
    return gather(json.loads(data_path.read_text(encoding="utf-8")))


def run_generator():
    from generator import generate
    return generate()



def run_llm():
    """Generate Spanish descriptions for businesses using LLM."""
    from llm_content import enrich
    return enrich()


def run_demo():
    from generator import generate as gen
    demos = [
        {
            "place_id": "demo-1", "name": "Restaurante El Raco",
            "category": "restaurante", "rating": 4.5, "reviews": 127,
            "address": "Carrer Sant Pere, 24, 46800 Xativa, Valencia",
            "phone": "+34 962 27 14 32", "type": "Restaurante mediterraneo",
            "hours": ["Lunes: 13:00-16:00", "Martes: 13:00-16:00, 20:00-23:00",
                      "Miercoles: 13:00-16:00, 20:00-23:00",
                      "Jueves: 13:00-16:00, 20:00-23:00",
                      "Viernes: 13:00-16:00, 20:00-23:30",
                      "Sabado: 13:00-16:00, 20:00-23:30", "Domingo: Cerrado"],
            "photos": ["https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
                       "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800"],
            "description": "Cocina mediterranea de temporada. Arroces, fideuas y platos tradicionales en el casco historico de Xativa. Ingredientes frescos del mercado y recetas de la abuela que han pasado de generacion en generacion.",
            "menu_items": [
                {"name": "Arroz del Senyoret", "description": "Arroz seco con gambas, cigalas y sepia, pelado a mano. Nuestro plato estrella.", "price": "16.50"},
                {"name": "Fideua Negra", "description": "Fideua con tinta de calamar, alioli casero y gambon fresco de la lonja.", "price": "15.00"},
                {"name": "Esgarraet", "description": "Pimientos rojos asados, bacalao desmigado, ajo y aceite de oliva virgen extra.", "price": "9.50"},
                {"name": "Croquetas de Puchero", "description": "Croquetas cremosas caseras hechas con la carne del cocido tradicional.", "price": "8.00"},
                {"name": "Torrija Caramelizada", "description": "Torrija de brioche con crema inglesa y helado de vainilla.", "price": "7.00"},
                {"name": "Menu del Dia", "description": "Primero, segundo, bebida y postre o cafe. De lunes a viernes.", "price": "13.90"}
            ],
            "faq": [
                {"question": "Teneis terraza?", "answer": "Si, disponemos de terraza exterior en la plaza. Perfecta para los meses de primavera y verano."},
                {"question": "Hay opciones vegetarianas?", "answer": "Si, tenemos varios platos vegetarianos en carta. Pregunta a nuestro personal."},
                {"question": "Se puede reservar?", "answer": "Recomendamos reservar especialmente fines de semana. Llamanos al 962 27 14 32."}
            ],
            "has_website": False, "website": None, "maps_url": "https://maps.google.com/?q=38.9889,-0.5157",
        },
        {
            "place_id": "demo-2", "name": "Perruqueria Estil",
            "category": "peluqueria", "rating": 4.8, "reviews": 53,
            "address": "Avinguda de Selgas, 12, 46800 Xativa, Valencia",
            "phone": "+34 962 28 91 45", "type": "Peluqueria unisex",
            "hours": ["Lunes: Cerrado", "Martes: 09:30-13:30, 16:00-20:00",
                      "Miercoles: 09:30-13:30, 16:00-20:00",
                      "Jueves: 09:30-13:30, 16:00-20:00",
                      "Viernes: 09:30-13:30, 16:00-20:00",
                      "Sabado: 09:30-14:00", "Domingo: Cerrado"],
            "photos": ["https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800"],
            "description": "15 anos cuidando tu imagen en el corazon de Xativa. Especialistas en coloracion, mechas balayage, tratamientos capilares y alisados. Trabajamos con productos profesionales de primeras marcas para garantizar los mejores resultados.",
            "services": [
                {"icon": "💇", "name": "Corte y Peinado", "description": "Corte personalizado + lavado + peinado. Asesoramiento de imagen incluido.", "price": "22€"},
                {"icon": "🎨", "name": "Coloracion", "description": "Tinte completo, mechas balayage, babylights, reflejos. Con productos sin amoniaco.", "price": "desde 38€"},
                {"icon": "✨", "name": "Tratamientos Capilares", "description": "Queratina, botox capilar, reestructuracion. Devuelve la vida a tu cabello.", "price": "desde 30€"},
                {"icon": "💆", "name": "Peinados de Fiesta", "description": "Recogidos, ondas, semirecogidos para bodas, bautizos y eventos.", "price": "desde 35€"},
                {"icon": "👰", "name": "Pack Novia", "description": "Prueba + peinado el gran dia + maquillaje profesional + tratamiento pre-boda.", "price": "desde 150€"},
                {"icon": "✂️", "name": "Arreglo de Barba", "description": "Perfilado, recorte, cuidado facial. Tambien hacemos caballero.", "price": "10€"}
            ],
            "faq": [
                {"question": "Hay que pedir cita?", "answer": "Si, trabajamos con cita previa para garantizar la mejor atencion. Puedes llamarnos o enviar un WhatsApp."},
                {"question": "Cuanto dura un tratamiento de queratina?", "answer": "Entre 2 y 4 meses dependiendo del tipo de cabello y los cuidados posteriores."}
            ],
            "has_website": False, "website": None, "maps_url": "https://maps.google.com/?q=38.9895,-0.5160",
        },
        {
            "place_id": "demo-3", "name": "Electricitat Navarro",
            "category": "electricista", "rating": 4.9, "reviews": 34,
            "address": "Carrer de la Reina, 8, 46800 Xativa, Valencia",
            "phone": "+34 610 55 42 87", "type": "Electricista",
            "hours": ["Lunes-Viernes: 09:00-19:00", "Sabado: 09:00-14:00", "Urgencias: 24h"],
            "photos": ["https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=800"],
            "description": "Servicios electricos profesionales en Xativa y toda la comarca de La Costera. Instalaciones nuevas, reformas, averias urgentes y boletines electricos (CIE). Servicio 24 horas para urgencias. Electricistas certificados con mas de 20 anos de experiencia.",
            "services": [
                {"icon": "⚡", "name": "Urgencias 24h", "description": "Averias electricas urgentes. Cortocircuitos, saltos de diferencial, apagones. Respuesta en menos de 1 hora.", "price": ""},
                {"icon": "🔌", "name": "Instalaciones Nuevas", "description": "Instalaciones electricas completas para viviendas, locales y naves. Proyectos y memorias tecnicas.", "price": ""},
                {"icon": "🛠️", "name": "Reformas", "description": "Renovacion de instalaciones antiguas, cambio de cuadros electricos, domotizacion.", "price": ""},
                {"icon": "📋", "name": "Boletines CIE", "description": "Emitimos certificados de instalacion electrica y boletines oficiales para contratos de luz.", "price": ""},
                {"icon": "🔋", "name": "Mantenimiento", "description": "Contratos de mantenimiento para comunidades, empresas y negocios. Evita averias antes de que ocurran.", "price": ""},
                {"icon": "💡", "name": "Iluminacion LED", "description": "Sustitucion e instalacion de iluminacion LED de bajo consumo. Ahorra hasta un 80% en tu factura.", "price": ""}
            ],
            "faq": [
                {"question": "Cuanto tardan en llegar para una urgencia?", "answer": "En Xativa capital llegamos en menos de 1 hora. Para pueblos de la comarca, entre 1 y 2 horas."},
                {"question": "Dan garantia de sus trabajos?", "answer": "Si, todos nuestros trabajos tienen garantia por escrito de 2 anos."},
                {"question": "Hacen presupuestos sin compromiso?", "answer": "Si, nos desplaciamos sin coste para valorar el trabajo y damos presupuesto detallado sin compromiso."},
                {"question": "Que zonas cubren?", "answer": "Xativa y toda la comarca de La Costera: Canals, L'Alcudia de Crespins, Moixent, Vallada, Genoves, El Genoves, y pueblos cercanos."}
            ],
            "has_website": False, "website": None, "maps_url": "https://maps.google.com/?q=38.9880,-0.5150",
        },
    ]
    print("\nGenerando 3 paginas de demo...\n")
    return gen(demos, only_without_website=False)



def run_deploy():
    """Deploy generated pages to Vercel."""
    from deploy import deploy
    import os
    token = os.environ.get("VERCEL_TOKEN", "")
    if len(sys.argv) > 2:
        token = sys.argv[2]
    if not token:
        print("Set VERCEL_TOKEN or pass as: python pipeline.py deploy <token>")
        return
    return deploy(token)


def run_full():
    print("=" * 60)
    print("  localbiz-web — Pipeline completo")
    print("=" * 60)
    run_discovery()
    run_checker()
    run_gatherer()
    run_generator()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "full"
    commands = {
        "discover": run_discovery, "check": run_checker,
        "gather": run_gatherer, "generate": run_generator,
        "deploy": run_deploy,
        "llm": run_llm,
        "demo": run_demo, "full": run_full,
    }
    if cmd not in commands:
        print(f"Comando desconocido: {cmd}")
        print(f"Opciones: {', '.join(commands.keys())}")
        sys.exit(1)
    commands[cmd]()


if __name__ == "__main__":
    main()
