#!/usr/bin/env python3
"""
BetMGM Selenium reconnaissance scraper v2.

Purpose:
    Render the public BetMGM football page with Selenium and extract
    structured event/market candidates from the rendered DOM.

This remains reconnaissance code. It deliberately preserves raw HTML/text
and writes a structured candidate JSON so we can compare extraction quality
before promoting anything to production acquisition code.
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


def clean_text(value):
    return re.sub(r"\s+", " ", (value or "")).strip()


def safe_filename(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value)[:100].strip("_") or "betmgm"


def extract_event_id(url):
    if not url:
        return None
    match = re.search(r":(\d+)(?:[/?#]|$)", url)
    return match.group(1) if match else None


def first_href(element):
    try:
        return element.get_attribute("href")
    except Exception:
        return None


def extract_markets(event):
    """
    Best-effort DOM extraction. BetMGM's markup can change, so preserve the
    complete event text and HTML clues even when a market isn't recognized.
    """
    result = {
        "spread": [],
        "total": [],
        "moneyline": [],
    }

    # Search descendants for common market labels. The exact component tree
    # is intentionally not assumed to be permanent.
    descendants = event.find_elements(By.XPATH, ".//*")
    for node in descendants:
        try:
            text = clean_text(node.text)
            if not text:
                continue

            low = text.lower()
            if low in {"spread", "total", "money", "moneyline"}:
                # Save the nearest useful parent text as an extraction clue.
                try:
                    parent_text = clean_text(
                        node.find_element(By.XPATH, "..").text
                    )
                except Exception:
                    parent_text = ""
                clue = {
                    "label": text,
                    "parent_text": parent_text[:1000],
                }

                if low == "spread":
                    result["spread"].append(clue)
                elif low == "total":
                    result["total"].append(clue)
                else:
                    result["moneyline"].append(clue)

    return result


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

        # Preserve the same core artifacts from v1.
        prefix = output_dir / f"betmgm_probe_{stamp}"
        prefix.with_suffix(".html").write_text(html, encoding="utf-8")
        prefix.with_suffix(".txt").write_text(body_text, encoding="utf-8")
        driver.save_screenshot(str(prefix.with_suffix(".png")))

        # Find rendered event wrappers. We use several selectors because
        # production markup may change while retaining the same semantics.
        selectors = [
            "div.grid-event-wrapper",
            "[class*='grid-event-wrapper']",
            "ms-event-detail",
        ]

        raw_events = []
        seen = set()

        for selector in selectors:
            for event in driver.find_elements(By.CSS_SELECTOR, selector):
                try:
                    event_html = event.get_attribute("outerHTML") or ""
                    event_text = clean_text(event.text)
                    hrefs = [
                        first_href(a)
                        for a in event.find_elements(By.TAG_NAME, "a")
                    ]
                    hrefs = [h for h in hrefs if h]

                    event_url = next(
                        (h for h in hrefs if "/sports/events/" in h),
                        None,
                    )
                    event_id = extract_event_id(event_url)

                    # Use URL when available; otherwise use a hash-like
                    # signature based on text to prevent duplicate selectors.
                    signature = event_url or event_text[:500]
                    if signature in seen:
                        continue
                    seen.add(signature)

                    markets = extract_markets(event)

                    raw_events.append({
                        "event_id": event_id,
                        "event_url": event_url,
                        "event_text": event_text[:3000],
                        "markets": markets,
                        "html_length": len(event_html),
                    })
                except Exception as exc:
                    print(f"Event extraction warning: {exc}")

        structured = {
            "schema_version": "betmgm_probe_v2",
            "retrieved_at_utc": timestamp.isoformat(),
            "requested_url": url,
            "final_url": driver.current_url,
            "page_title": driver.title,
            "wait_seconds": wait_seconds,
            "event_count": len(raw_events),
            "events": raw_events,
        }

        structured_path = output_dir / f"betmgm_events_{stamp}.json"
        structured_path.write_text(
            json.dumps(structured, indent=2, ensure_ascii=False),
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
            "event_count": len(raw_events),
            "selectors_checked": selectors,
        }

        (output_dir / f"betmgm_probe_{stamp}_metadata.json").write_text(
            json.dumps(metadata, indent=2), encoding="utf-8"
        )

        print("\n=== BetMGM probe v2 complete ===")
        print(json.dumps(metadata, indent=2))
        print(f"Structured candidate data: {structured_path}")

        for event in raw_events[:10]:
            print(
                f"- {event['event_id']} | "
                f"{event['event_url']} | "
                f"{event['event_text'][:160]}"
            )

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
