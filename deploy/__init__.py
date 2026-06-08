"""Deploy module — uploads generated pages to Vercel."""

import json
import subprocess
import sys
from pathlib import Path

import config


def build_index(html_dir: Path) -> Path:
    """Build an index.html linking to all generated pages."""
    pages = sorted(html_dir.glob("*.html"))
    # Filter out index itself
    pages = [p for p in pages if p.name != "index.html"]

    links = []
    for p in pages:
        name = p.stem.replace("-", " ").title()
        links.append(f'<li><a href="{p.name}">{name}</a></li>')

    index_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Negocios en {config.CITY} — localbiz-web</title>
    <style>
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f8fafc; color: #1e293b; }}
        h1 {{ color: #2563eb; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin: 8px 0; }}
        a {{ display: block; padding: 12px 16px; background: white; border-radius: 8px; text-decoration: none; color: #2563eb; font-weight: 500; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        a:hover {{ background: #2563eb; color: white; }}
        .count {{ color: #64748b; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <h1>Negocios en {config.CITY}</h1>
    <p class="count">{len(pages)} paginas generadas</p>
    <ul>
{chr(10).join(links)}
    </ul>
    <p style="margin-top:40px;color:#94a3b8;font-size:0.85rem;">Generado con localbiz-web · {config.CITY}, {config.REGION}</p>
</body>
</html>"""

    index_path = html_dir / "index.html"
    index_path.write_text(index_html, encoding="utf-8")
    return index_path


def deploy(vercel_token: str = None, prod: bool = True) -> str:
    """Deploy output/html/ to Vercel. Returns the deployment URL."""
    html_dir = Path(config.HTML_DIR)
    if not html_dir.exists() or not list(html_dir.glob("*.html")):
        print("No HTML pages to deploy. Run generator first.")
        return ""

    # Build index
    build_index(html_dir)
    print(f"Index built with {len(list(html_dir.glob('*.html'))) - 1} pages")

    # Get token
    if not vercel_token:
        # Try env var
        import os
        vercel_token = os.environ.get("VERCEL_TOKEN", "")
        if not vercel_token:
            print("Set VERCEL_TOKEN env var or pass token to deploy()")
            return ""

    # Deploy using npx vercel
    cmd = [
        "npx", "--yes", "vercel",
        "--token", vercel_token,
        "--cwd", str(html_dir),
        "--yes",
    ]
    if prod:
        cmd.append("--prod")

    print(f"Deploying to Vercel...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        print(f"Deploy failed: {result.stderr}")
        return ""

    # Extract URL from output
    output = result.stdout + result.stderr
    url = ""
    for line in output.split("\n"):
        if "Production" in line or "Aliased" in line:
            url = line.split("https://")[-1].strip()
            if url:
                url = "https://" + url.split()[0]
                break

    if url:
        print(f"Deployed: {url}")
        for p in sorted(html_dir.glob("*.html")):
            if p.name != "index.html":
                print(f"  {url}/{p.name}")
    else:
        print(f"Deploy output:\n{output[:500]}")

    return url


def deploy_demo(token: str = None) -> str:
    """Quick deploy of existing pages with index."""
    return deploy(token, prod=True)


if __name__ == "__main__":
    token = sys.argv[1] if len(sys.argv) > 1 else None
    deploy(token)
