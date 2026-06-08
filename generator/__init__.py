"""Generator module — creates HTML landing pages with Jinja2."""

import json
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

import config


def slugify(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    return slug[:80]


def generate_one(business: dict) -> Path:
    templates_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("landing.html.j2")

    html = template.render(
        business=business,
        city=config.CITY,
        region=config.REGION,
        country=config.COUNTRY,
    )

    output_dir = Path(config.HTML_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{slugify(business['name'])}.html"
    output_path = output_dir / filename
    output_path.write_text(html, encoding="utf-8")
    return output_path


def generate(businesses=None, limit=None, only_without_website=True) -> list[Path]:
    if businesses is None:
        for fname in ["gathered.json", "checked.json"]:
            data_path = Path(config.DATA_DIR) / fname
            if data_path.exists():
                businesses = json.loads(data_path.read_text(encoding="utf-8"))
                break
        else:
            print("No data found. Run discovery -> checker -> gatherer first.")
            return []

    if only_without_website:
        businesses = [b for b in businesses if not b.get("has_website", False)]

    if limit:
        businesses = businesses[:limit]

    total = len(businesses)
    print(f"\nGenerating {total} HTML pages...\n")

    outputs = []
    for i, biz in enumerate(businesses, 1):
        name = biz["name"]
        try:
            path = generate_one(biz)
            outputs.append(path)
            has_photos = len(biz.get("photos", []))
            print(f"  [{i}/{total}] {name} -> {path.name}{' [photos]' if has_photos else ''}")
        except Exception as e:
            print(f"  [{i}/{total}] {name} ERROR: {e}")

    print(f"\nDone: {len(outputs)} pages generated in {Path(config.HTML_DIR).resolve()}/")
    return outputs
