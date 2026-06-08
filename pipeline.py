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
            "photos": ["https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=1200", "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800", "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800", "https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=800", "https://images.unsplash.com/photo-1424847651672-bf20a4b0982b?w=800",
                       "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800"],
            "description": "El Raco es esa esquina del casco antiguo de Xativa donde siempre huele a algo bueno. Llevamos desde 1998 cocinando lo que nos enseno la abuela: arroces de fuego lento, fideuas de la lonja, croquetas que se deshacen. No hay carta interminable ni pretensiones. Hay producto de aqui, recetas de siempre y una terraza donde se esta mejor que en casa. Ven a comer, que para eso estamos.",
            "menu_categories": [
                {"name": "Entrantes", "items": [
                    {"name": "Esgarraet de la Casa", "description": "Pimientos rojos asados al horno de lena, bacalao desmigado del Cantabrico, ajo confitado y aceite de oliva virgen extra de la Sierra de Mariola.", "price": "9.50", "image": "https://images.unsplash.com/photo-1534080564583-6be75777b70a?w=600"},
                    {"name": "Croquetas de Puchero", "description": "Cremosas por dentro, crujientes por fuera. Las hace la abuela cada manana con la carne del cocido tradicional.", "price": "8.00", "image": "https://images.unsplash.com/photo-1604909052743-94e838986d24?w=600"},
                    {"name": "Ensalada de la Huerta", "description": "Tomate valenciano, cebolla tierna, aceitunas de la comarca, ventresca de bonito del norte. Simple, fresca, perfecta.", "price": "7.50", "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600"}
                ]},
                {"name": "Arroces y Fideuas", "items": [
                    {"name": "Arroz del Senyoret", "description": "Nuestro plato insignia. Arroz seco con gambas, cigalas y sepia, todo pelado a mano para que no tengas que mancharte los dedos. Caldo de pescado de roca hecho a fuego lento.", "price": "16.50", "image": "https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=600"},
                    {"name": "Fideua Negra", "description": "Fideua de tinta de calamar con alioli casero de ajo morado. Gambon fresco de la lonja de Gandia. La receta que nos enseno el tio Pepe.", "price": "15.00", "image": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600"},
                    {"name": "Arroz con Verduras", "description": "De la huerta a la mesa. Alcachofa, habas, pimiento, ajetes tiernos. Caldo vegetal casero. Vegano y delicioso.", "price": "13.00", "image": "https://images.unsplash.com/photo-1594041680534-e8c8cdebd659?w=600"}
                ]},
                {"name": "Postres Caseros", "items": [
                    {"name": "Torrija Caramelizada", "image": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=600", "description": "Brioche empapado en leche infusionada con canela y limon. Caramelo crujiente, crema inglesa y helado de vainilla. Hecha al momento.", "price": "7.00", "image": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=600"},
                    {"name": "Tarta de Queso", "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=600", "description": "Estilo La Vina. Solo cinco ingredientes. Cremosa por dentro, tostada por fuera. No podemos dejar de hacerla.", "price": "6.50", "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=600"}
                ]},
                {"name": "Menu del Dia", "items": [
                    {"name": "Menu del Dia", "image": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600", "description": "Primero, segundo, bebida y postre o cafe. De lunes a viernes. Cambia cada semana segun lo que trae el mercado.", "price": "13.90", "image": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600"}
                ]}
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
            "description": "Llevamos 15 años en el mismo sitio y no pensamos movernos. Aquí no hacemos peinados de pasarela ni te vendemos productos que no necesitas. Te escuchamos, te aconsejamos y te dejamos el pelo exactamente como querías. Trabajamos con primeras marcas porque tu pelo se lo merece, y tratamos a cada clienta como si fuera la única. Pide cita y ven a contarnos qué necesitas.",
            "services": [
                {"icon": "💇", "name": "Corte y Peinado", "description": "Corte personalizado + lavado + peinado. Te escuchamos antes de tocar la tijera. Asesoramiento de imagen incluido sin coste.", "price": "22€", "image": "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=600"},
                {"icon": "🎨", "name": "Coloración", "description": "Tinte completo, mechas balayage, babylights, reflejos. Solo trabajamos con productos sin amoniaco. El color que buscas, sin dañar tu pelo.", "price": "desde 38€", "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600"},
                {"icon": "✨", "name": "Tratamientos Capilares", "description": "Queratina, botox capilar, reestructuración. Devuelve la vida a tu cabello en una sola sesión. Resultados visibles desde el primer día.", "price": "desde 30€", "image": "https://images.unsplash.com/photo-1605497788044-5a32c7078486?w=600"},
                {"icon": "💆", "name": "Peinados de Fiesta", "description": "Recogidos, ondas, semirecogidos para bodas, bautizos y eventos especiales. Ven con tiempo, hacemos prueba previa.", "price": "desde 35€", "image": "https://images.unsplash.com/photo-1485968579580-b6d095142e6e?w=600"},
                {"icon": "👰", "name": "Pack Novia", "description": "Prueba de peinado + maquillaje profesional + tratamiento pre-boda. El gran día es tuyo, nosotras nos encargamos de que brilles.", "price": "desde 150€", "image": "https://images.unsplash.com/photo-1595475884562-073c30d45670?w=600"},
                {"icon": "✂️", "name": "Arreglo de Barba", "description": "Perfilado, recorte, cuidado facial con productos específicos. Porque ellos también se cuidan. También hacemos caballero completo.", "price": "10€", "image": "https://images.unsplash.com/photo-1621605815971-fbc98d665594?w=600"}
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
            "description": "Más de 20 años enchufando Xàtiva. Literalmente. Nos llaman cuando se va la luz en plena cena de Navidad, cuando hay que reformar una casa entera, cuando toca pasar el boletín. Llegamos rápido, miramos el problema, te contamos qué pasa sin tecnicismos y te damos presupuesto en el momento. Urgencias 24h porque las averías no avisan. Y nunca, nunca cobramos el desplazamiento.",
            "services": [
                {"icon": "⚡", "name": "Urgencias 24h", "description": "Averías eléctricas urgentes. Cortocircuitos, saltos de diferencial, apagones. Respuesta en menos de 1 hora. No cobramos desplazamiento.", "price": "", "image": "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=600"},
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
