#!/usr/bin/env python3
"""
BetMGM Selenium reconnaissance scraper v3 — NCAAF.

Same workflow interface as v1/v2. The probe is now aimed specifically at
college football and deduplicates event records by stable event URL/ID.

Raw rendered artifacts are preserved. Structured extraction remains
reconnaissance-only.
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


DEFAULT_URL = "https://www.betmgm.com/en/sports/football-11/ncaaf"


def clean_text(value):
    return re.sub(r"\s+", " ", (value or "")).strip()


def extract_event_id(url):
    if not url:
        return None
    match = re.search(r":(\d+)(?:[/?#]|$)", url)
    return match.group(1) if match else None


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

        prefix = output_dir / f"betmgm_probe_{stamp}"
        prefix.with_suffix(".html").write_text(html, encoding="utf-8")
        prefix.with_suffix(".txt").write_text(body_text, encoding="utf-8")
        driver.save_screenshot(str(prefix.with_suffix(".png")))

        selectors = [
            "div.grid-event-wrapper",
            "[class*='grid-event-wrapper']",
            "ms-event-detail",
        ]

        events_by_id = {}
        anonymous_candidates = []

        for selector in selectors:
            print(f"Checking selector: {selector}")

            for event in driver.find_elements(By.CSS_SELECTOR, selector):
                try:
                    event_text = clean_text(event.text)
                    event_html = event.get_attribute("outerHTML") or ""

                    hrefs = []
                    for anchor in event.find_elements(By.TAG_NAME, "a"):
                        href = anchor.get_attribute("href")
                        if href:
                            hrefs.append(href)

                    event_url = next(
                        (
                            href for href in hrefs
                            if "/sports/events/" in href
                        ),
                        None,
                    )

                    event_id = extract_event_id(event_url)

                    record = {
                        "event_id": event_id,
                        "event_url": event_url,
                        "event_text": event_text[:3000],
                        "html_length": len(event_html),
                        "selector": selector,
                    }

                    if event_id or event_url:
                        key = event_id or event_url
                        if key not in events_by_id:
                            events_by_id[key] = record
                    else:
                        # Preserve anonymous candidates for diagnostics, but
                        # do not count them as real events.
                        if event_text:
                            anonymous_candidates.append(record)

                except Exception as exc:
                    print(f"Event extraction warning: {exc}")

        events = list(events_by_id.values())

        structured = {
            "schema_version": "betmgm_probe_v3_ncaaf",
            "retrieved_at_utc": timestamp.isoformat(),
            "requested_url": url,
            "final_url": driver.current_url,
            "page_title": driver.title,
            "sport_target": "NCAAF",
            "wait_seconds": wait_seconds,
            "event_count": len(events),
            "anonymous_candidate_count": len(anonymous_candidates),
            "events": events,
            "anonymous_candidates": anonymous_candidates,
        }

        structured_path = (
            output_dir / f"betmgm_ncaaf_events_{stamp}.json"
        )
        structured_path.write_text(
            json.dumps(structured, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        metadata = {
            "retrieved_at_utc": timestamp.isoformat(),
            "requested_url": url,
            "final_url": driver.current_url,
            "page_title": driver.title,
            "sport_target": "NCAAF",
            "wait_seconds": wait_seconds,
            "html_bytes": len(html.encode("utf-8")),
            "body_text_chars": len(body_text),
            "unique_event_count": len(events),
            "anonymous_candidate_count": len(anonymous_candidates),
            "selectors_checked": selectors,
        }

        metadata_path = (
            output_dir / f"betmgm_probe_{stamp}_metadata.json"
        )
        metadata_path.write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

        print("\n=== BetMGM NCAAF probe v3 complete ===")
        print(json.dumps(metadata, indent=2))
        print(f"Structured candidate data: {structured_path}")

        for event in events[:25]:
            print(
                f"- {event['event_id']} | "
                f"{event['event_url']} | "
                f"{event['event_text'][:160]}"
            )

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
