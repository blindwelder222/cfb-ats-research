#!/usr/bin/env python3
"""
BetMGM Selenium reconnaissance scraper v3.1 — navigation discovery.

Purpose:
    Inspect the rendered BetMGM page to discover how sports/category
    navigation is represented in the DOM.

This is intentionally a reconnaissance tool. It does not assume that
NCAAF has a particular URL. It inventories anchors, buttons, ARIA roles,
data attributes, and navigation-related text so we can discover the
actual route/control used by BetMGM.

The existing workflow interface is preserved.
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


DEFAULT_URL = "https://www.betmgm.com/en/sports/football-11"

KEYWORDS = (
    "ncaaf",
    "ncaa",
    "college",
    "football",
    "nfl",
    "cfl",
)


def clean_text(value):
    return re.sub(r"\s+", " ", (value or "")).strip()


def visible(element):
    try:
        return bool(element.is_displayed())
    except Exception:
        return False


def element_record(element, tag_name=None):
    try:
        tag = tag_name or element.tag_name
    except Exception:
        tag = tag_name

    record = {
        "tag": tag,
        "text": clean_text(getattr(element, "text", "") or ""),
        "visible": visible(element),
    }

    attributes = (
        "href",
        "aria-label",
        "aria-labelledby",
        "role",
        "title",
        "data-testid",
        "routerlink",
        "ng-reflect-router-link",
        "class",
        "id",
    )

    for attribute in attributes:
        try:
            value = element.get_attribute(attribute)
            if value is not None and value != "":
                record[attribute] = value
        except Exception:
            pass

    return record


def keyword_matches(record):
    haystack = " ".join(
        str(record.get(key, ""))
        for key in record
        if key != "visible"
    ).lower()

    return [
        keyword for keyword in KEYWORDS
        if keyword in haystack
    ]


def main():
    url = os.getenv("BETMGM_URL", DEFAULT_URL)
    wait_seconds = float(os.getenv("WAIT_SECONDS", "8"))
    output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc)
    stamp = timestamp.strftime("%Y%m%dT%H%M%SZ")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    try:
        print(f"Opening: {url}")
        driver.get(url)

        print(f"Waiting {wait_seconds} seconds for JavaScript...")
        time.sleep(wait_seconds)

        html = driver.page_source
        body_text = clean_text(
            driver.find_element(By.TAG_NAME, "body").text
        )

        prefix = output_dir / f"betmgm_nav_probe_{stamp}"

        # Preserve raw rendered evidence.
        prefix.with_suffix(".html").write_text(
            html, encoding="utf-8"
        )
        prefix.with_suffix(".txt").write_text(
            body_text, encoding="utf-8"
        )
        driver.save_screenshot(str(prefix.with_suffix(".png")))

        # Inventory anchors.
        anchors = [
            element_record(element, "a")
            for element in driver.find_elements(By.TAG_NAME, "a")
        ]

        # Inventory buttons.
        buttons = [
            element_record(element, "button")
            for element in driver.find_elements(By.TAG_NAME, "button")
        ]

        # Inventory elements explicitly marked as link/button roles.
        role_elements = []
        for role in ("link", "button"):
            for element in driver.find_elements(
                By.CSS_SELECTOR, f'[role="{role}"]'
            ):
                role_elements.append(element_record(element))

        # Inventory elements with navigation-related Angular/data attributes.
        attribute_elements = []
        selectors = [
            "[routerlink]",
            "[ng-reflect-router-link]",
            "[data-testid]",
            "[aria-label]",
        ]

        seen_attribute_elements = set()

        for selector in selectors:
            for element in driver.find_elements(By.CSS_SELECTOR, selector):
                try:
                    signature = (
                        element.tag_name,
                        element.get_attribute("outerHTML")[:500],
                    )
                except Exception:
                    signature = id(element)

                if signature in seen_attribute_elements:
                    continue

                seen_attribute_elements.add(signature)
                attribute_elements.append(element_record(element))

        # Search for likely sports/category navigation references.
        keyword_hits = []

        all_records = (
            [("anchor", record) for record in anchors]
            + [("button", record) for record in buttons]
            + [("role", record) for record in role_elements]
            + [("attribute", record) for record in attribute_elements]
        )

        seen_hits = set()

        for source_type, record in all_records:
            matches = keyword_matches(record)
            if not matches:
                continue

            signature = json.dumps(
                record,
                sort_keys=True,
                ensure_ascii=False,
            )

            if signature in seen_hits:
                continue

            seen_hits.add(signature)

            keyword_hits.append(
                {
                    "source_type": source_type,
                    "matched_keywords": matches,
                    "element": record,
                }
            )

        result = {
            "schema_version": "betmgm_navigation_probe_v3_1",
            "retrieved_at_utc": timestamp.isoformat(),
            "requested_url": url,
            "final_url": driver.current_url,
            "page_title": driver.title,
            "wait_seconds": wait_seconds,
            "counts": {
                "anchors": len(anchors),
                "buttons": len(buttons),
                "role_elements": len(role_elements),
                "attribute_elements": len(attribute_elements),
                "keyword_hits": len(keyword_hits),
            },
            "keyword_hits": keyword_hits,
            "anchors": anchors,
            "buttons": buttons,
            "role_elements": role_elements,
            "attribute_elements": attribute_elements,
        }

        json_path = (
            output_dir / f"betmgm_navigation_{stamp}.json"
        )
        json_path.write_text(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        metadata = {
            "retrieved_at_utc": timestamp.isoformat(),
            "requested_url": url,
            "final_url": driver.current_url,
            "page_title": driver.title,
            "wait_seconds": wait_seconds,
            "html_bytes": len(html.encode("utf-8")),
            "body_text_chars": len(body_text),
            "counts": result["counts"],
        }

        metadata_path = (
            output_dir / f"betmgm_nav_probe_{stamp}_metadata.json"
        )
        metadata_path.write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

        print("\n=== BetMGM navigation probe v3.1 complete ===")
        print(json.dumps(metadata, indent=2))

        print("\n=== Keyword navigation hits ===")
        for hit in keyword_hits:
            record = hit["element"]
            print(
                f"[{hit['source_type']}] "
                f"{hit['matched_keywords']} "
                f"text={record.get('text', '')[:100]!r} "
                f"href={record.get('href', '')!r} "
                f"aria={record.get('aria-label', '')!r} "
                f"testid={record.get('data-testid', '')!r}"
            )

        print(f"\nFull navigation inventory: {json_path}")
        print(f"Metadata: {metadata_path}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
