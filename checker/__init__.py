"""Checker module — detects which businesses lack a website."""

import json
import time
from pathlib import Path
from typing import Optional

import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

import config


def find_website_playwright(business: dict) -> Optional[str]:
    place_id = business.get("place_id", "")
    if not place_id:
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=config.HEADLESS)
            context = browser.new_context(
                viewport=config.VIEWPORT,
                user_agent=config.USER_AGENT,
                locale="es-ES",
            )
            page = context.new_page()

            url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            page.goto(url, wait_until="domcontentloaded", timeout=config.TIMEOUT)
            time.sleep(3)

            website_link = page.query_selector(
                'a[data-item-id="authority"], a[href*="http"][aria-label*="Web"], '
                'a[data-tooltip="Abrir sitio web"], a[aria-label*="Sitio web"]'
            )

            website = None
            if website_link:
                website = website_link.get_attribute("href")
            else:
                all_links = page.query_selector_all('a[href^="http"]')
                for link in all_links:
                    href = link.get_attribute("href") or ""
                    if "google.com" not in href and "maps.google" not in href:
                        text = link.inner_text().strip() if link.inner_text() else ""
                        if text and len(href) > 10:
                            website = href
                            break

            browser.close()
            return website
    except Exception as e:
        print(f"    Error: {e}")
        return None


def check_website_reachable(url: str) -> bool:
    if not url or not url.startswith("http"):
        return False
    try:
        resp = requests.get(
            url,
            timeout=config.WEBSITE_TIMEOUT,
            headers={"User-Agent": config.USER_AGENT},
            allow_redirects=True,
        )
        return resp.status_code < 500
    except requests.RequestException:
        return False


def check_business(business: dict, index: int, total: int) -> dict:
    name = business["name"]
    print(f"  [{index}/{total}] {name}...", end=" ")

    website = find_website_playwright(business)
    has_website = False

    if website:
        has_website = check_website_reachable(website)
        print(f"OK {website}" if has_website else "unreachable")
    else:
        print("no website")

    business["website"] = website
    business["has_website"] = has_website
    return business


def check(businesses: list[dict] = None, limit: int = None) -> list[dict]:
    if businesses is None:
        data_path = Path(config.DATA_DIR) / "discovered.json"
        if not data_path.exists():
            print(f"Not found: {data_path}. Run discovery first.")
            return []
        businesses = json.loads(data_path.read_text(encoding="utf-8"))

    if limit:
        businesses = businesses[:limit]

    total = len(businesses)
    print(f"\nChecking {total} businesses...\n")

    results = []
    for i, biz in enumerate(businesses, 1):
        result = check_business(biz, i, total)
        results.append(result)

    output_path = Path(config.DATA_DIR) / "checked.json"
    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    no_web = [b for b in results if not b["has_website"]]
    with_web = [b for b in results if b["has_website"]]
    pct = len(no_web) / len(results) * 100 if results else 0
    print(f"\nResults: {len(with_web)} with website, {len(no_web)} without ({pct:.0f}%)\n")
    return results
