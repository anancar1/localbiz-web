"""Discovery module — scrapes Google Maps for local businesses."""

import json
import time
import random
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

import config


def search_url(category: str) -> str:
    query = f"{category} en {config.CITY}, {config.REGION}"
    return f"https://www.google.com/maps/search/{query.replace(' ', '+')}"


def extract_results(page, max_results: int = 30) -> list[dict]:
    businesses = []
    seen_place_ids = set()

    try:
        page.wait_for_selector('[role="feed"]', timeout=config.TIMEOUT)
    except PlaywrightTimeout:
        print("  No results feed found")
        return businesses

    scroll_attempts = 0
    while len(businesses) < max_results and scroll_attempts < 15:
        feed = page.query_selector('[role="feed"]')
        if feed:
            cards = feed.query_selector_all('[role="article"]')
            for card in cards:
                try:
                    link = card.query_selector('a[href*="/place/"]')
                    if not link:
                        continue
                    href = link.get_attribute("href") or ""
                    if "/place/" not in href:
                        continue

                    place_id = None
                    place_link = card.query_selector('a[data-place-id]')
                    if place_link:
                        place_id = place_link.get_attribute("data-place-id")
                    else:
                        parts = href.split("/place/")
                        if len(parts) > 1:
                            place_id = parts[1].split("/")[0]

                    if not place_id or place_id in seen_place_ids:
                        continue
                    seen_place_ids.add(place_id)

                    name_el = card.query_selector('[aria-label]')
                    name = name_el.get_attribute("aria-label") if name_el else ""
                    if not name:
                        heading = card.query_selector('div.fontHeadlineSmall, span.fontHeadlineSmall')
                        if heading:
                            name = heading.inner_text()
                    if not name:
                        continue

                    rating = None
                    rating_el = card.query_selector('[role="img"][aria-label*="stars"], [role="img"][aria-label*="estrellas"]')
                    if rating_el:
                        rating_text = rating_el.get_attribute("aria-label") or ""
                        try:
                            rating = float(rating_text.split()[0].replace(",", "."))
                        except (ValueError, IndexError):
                            pass

                    reviews = None
                    review_el = card.query_selector('span[aria-label*="reviews"], span[aria-label*="reseñas"]')
                    if review_el:
                        review_text = review_el.get_attribute("aria-label") or review_el.inner_text()
                        try:
                            nums = "".join(c for c in review_text if c.isdigit())
                            reviews = int(nums) if nums else None
                        except ValueError:
                            pass

                    address = ""
                    addr_spans = card.query_selector_all('div.W4Efsd span')
                    for s in addr_spans:
                        txt = s.inner_text().strip()
                        if txt and (", " in txt or "C/" in txt or "Calle" in txt or "Av." in txt):
                            address = txt
                            break

                    category_text = ""
                    spans = card.query_selector_all('div.W4Efsd span')
                    for s in spans:
                        txt = s.inner_text().strip()
                        if txt and not txt.startswith("(") and "\u20ac" not in txt:
                            parts = [c.strip() for c in txt.split("\u00b7")]
                            for cp in parts:
                                if cp and not cp.replace(".", "").replace(",", "").isdigit():
                                    category_text = cp
                                    break
                            if category_text:
                                break

                    businesses.append({
                        "place_id": place_id,
                        "name": name,
                        "category": category,
                        "rating": rating,
                        "reviews": reviews,
                        "address": address,
                        "type": category_text,
                        "maps_url": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                    })

                    if len(businesses) >= max_results:
                        break
                except Exception:
                    continue

        if feed:
            try:
                page.evaluate("arguments[0].scrollBy(0, 800)", feed)
            except Exception:
                pass
        scroll_attempts += 1
        time.sleep(random.uniform(1.5, 3.0))

    return businesses


def discover(categories: list[str] = None) -> list[dict]:
    if categories is None:
        categories = config.CATEGORIES

    all_businesses = []
    Path(config.DATA_DIR).mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        context = browser.new_context(
            viewport=config.VIEWPORT,
            user_agent=config.USER_AGENT,
            locale="es-ES",
            timezone_id="Europe/Madrid",
        )
        page = context.new_page()

        for cat in categories:
            print(f"\n🔍 Searching: {cat} in {config.CITY}...")
            url = search_url(cat)
            page.goto(url, wait_until="domcontentloaded", timeout=config.TIMEOUT)
            time.sleep(random.uniform(2, 4))

            try:
                page.click('button:has-text("Aceptar"), button:has-text("Accept")', timeout=3000)
                time.sleep(1)
            except PlaywrightTimeout:
                pass

            results = extract_results(page, max_results=30)
            print(f"  Found {len(results)} businesses")
            all_businesses.extend(results)

        browser.close()

    output_path = Path(config.DATA_DIR) / "discovered.json"
    output_path.write_text(json.dumps(all_businesses, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n📁 {len(all_businesses)} businesses saved to {output_path}")
    return all_businesses
