"""Gatherer module — extracts detailed business info from Google Maps."""

import json
import time
import random
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

import config


def gather_business(business: dict) -> dict:
    place_id = business.get("place_id", "")
    if not place_id:
        return business

    result = dict(business)
    result.setdefault("phone", None)
    result.setdefault("address", None)
    result.setdefault("hours", [])
    result.setdefault("photos", [])
    result.setdefault("description", "")

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
            time.sleep(random.uniform(2.5, 4))

            # Phone
            try:
                phone_btn = page.query_selector(
                    'button[aria-label*="Telefono"], button[aria-label*="telefono"], '
                    'button[data-item-id="phone"], a[href^="tel:"]'
                )
                if phone_btn:
                    href = phone_btn.get_attribute("href") or ""
                    if "tel:" in href:
                        result["phone"] = href.replace("tel:", "")
                    else:
                        aria = phone_btn.get_attribute("aria-label") or ""
                        if any(c.isdigit() for c in aria):
                            result["phone"] = aria
                if not result["phone"]:
                    phone_text = page.query_selector('button[data-item-id="phone"] .fontBodyMedium')
                    if phone_text:
                        txt = phone_text.inner_text().strip()
                        if any(c.isdigit() for c in txt) and len(txt) >= 9:
                            result["phone"] = txt
            except Exception:
                pass

            # Address
            try:
                addr_btn = page.query_selector(
                    'button[data-item-id="address"], button[aria-label*="Direccion"]'
                )
                if addr_btn:
                    addr_spans = addr_btn.query_selector_all('[class*="font"]')
                    for s in addr_spans:
                        txt = s.inner_text().strip()
                        if txt and len(txt) > 5 and "Direccion" not in txt:
                            result["address"] = txt
                            break
            except Exception:
                pass

            # Hours
            try:
                hours_btn = page.query_selector(
                    'button[aria-label*="Horario"], div[aria-label*="Horario"] button'
                )
                if hours_btn:
                    hours_btn.click()
                    time.sleep(1.5)
                    hours_rows = page.query_selector_all('table tbody tr')
                    hours = [r.inner_text().strip() for r in hours_rows if r.inner_text().strip()]
                    if hours:
                        result["hours"] = hours
                    page.keyboard.press("Escape")
                    time.sleep(0.5)
            except Exception:
                pass

            # Photos
            try:
                photo_imgs = page.query_selector_all('img[src*="googleusercontent.com"]')
                photos = []
                for img in photo_imgs[:6]:
                    src = img.get_attribute("src")
                    if src and "googleusercontent" in src:
                        photos.append(src.split("=w")[0] + "=w800-h600-p")
                if photos:
                    result["photos"] = photos[:6]
            except Exception:
                pass

            # Description
            try:
                review_snippets = page.query_selector_all('[data-review-id]')
                if review_snippets:
                    desc_text = review_snippets[0].query_selector('[class*="fontBodyMedium"], span[lang]')
                    if desc_text:
                        result["description"] = desc_text.inner_text().strip()[:300]
            except Exception:
                pass

            browser.close()
    except Exception as e:
        print(f"    Error: {e}")

    return result


def gather(businesses: list[dict] = None, limit: int = None) -> list[dict]:
    if businesses is None:
        checked_path = Path(config.DATA_DIR) / "checked.json"
        if not checked_path.exists():
            print(f"Not found: {checked_path}. Run checker first.")
            return []
        businesses = json.loads(checked_path.read_text(encoding="utf-8"))

    no_web = [b for b in businesses if not b.get("has_website", False)]
    if limit:
        no_web = no_web[:limit]

    total = len(no_web)
    print(f"\nGathering data for {total} businesses without websites...\n")

    results = []
    for i, biz in enumerate(no_web, 1):
        name = biz["name"]
        print(f"  [{i}/{total}] {name}...")
        enriched = gather_business(biz)
        results.append(enriched)
        time.sleep(random.uniform(1, 2))

    with_web = [b for b in businesses if b.get("has_website", False)]
    all_results = with_web + results

    output_path = Path(config.DATA_DIR) / "gathered.json"
    output_path.write_text(json.dumps(all_results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nData saved to {output_path}")
    return results
