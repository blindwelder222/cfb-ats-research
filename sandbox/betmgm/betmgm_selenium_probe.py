#!/usr/bin/env python3
"""
Primitive BetMGM Selenium reconnaissance scraper.

Purpose:
    Load a public BetMGM sportsbook page in a real Chromium browser,
    wait for JavaScript to render, and save raw artifacts for inspection.

This is intentionally a reconnaissance tool, not a production scraper.
Once we identify the actual data source (DOM, embedded JSON, or network API),
we can replace Selenium with a lighter direct-request collector.
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


def safe_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value[:100].strip("_") or "betmgm"


def main():
    url = os.getenv("BETMGM_URL", DEFAULT_URL)
    wait_seconds = float(os.getenv("WAIT_SECONDS", "8"))

    timestamp = datetime.now(timezone.utc)
    stamp = timestamp.strftime("%Y%m%dT%H%M%SZ")

    output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

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

        title = driver.title
        current_url = driver.current_url
        html = driver.page_source
        text = driver.find_element(By.TAG_NAME, "body").text

        # Capture a simple inventory of links and visible elements.
        links = []
        for element in driver.find_elements(By.TAG_NAME, "a"):
            href = element.get_attribute("href")
            label = element.text.strip()
            if href or label:
                links.append({"text": label, "href": href})

        elements = []
        for element in driver.find_elements(By.CSS_SELECTOR, "[data-testid], [class]"):
            try:
                tag = element.tag_name
                testid = element.get_attribute("data-testid")
                classes = element.get_attribute("class")
                label = element.text.strip()
                if testid or classes:
                    elements.append({
                        "tag": tag,
                        "data-testid": testid,
                        "class": classes,
                        "text": label[:500],
                    })
            except Exception:
                pass

        metadata = {
            "retrieved_at_utc": timestamp.isoformat(),
            "requested_url": url,
            "final_url": current_url,
            "page_title": title,
            "wait_seconds": wait_seconds,
            "html_bytes": len(html.encode("utf-8")),
            "body_text_chars": len(text),
            "link_count": len(links),
            "element_inventory_count": len(elements),
        }

        prefix = output_dir / f"betmgm_probe_{stamp}"

        (prefix.with_suffix(".html")).write_text(html, encoding="utf-8")
        (prefix.with_suffix(".txt")).write_text(text, encoding="utf-8")
        (prefix.with_name(prefix.name + "_links.json")).write_text(
            json.dumps(links, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (prefix.with_name(prefix.name + "_elements.json")).write_text(
            json.dumps(elements, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (prefix.with_name(prefix.name + "_metadata.json")).write_text(
            json.dumps(metadata, indent=2), encoding="utf-8"
        )

        driver.save_screenshot(str(prefix.with_suffix(".png")))

        print("\n=== BetMGM probe complete ===")
        print(json.dumps(metadata, indent=2))
        print(f"Artifacts written to: {output_dir.resolve()}")

        # Print useful clues without attempting to interpret the site.
        lower = html.lower()
        clues = [
            "api", "graphql", "odds", "spread", "moneyline",
            "total", "event", "fixture", "market", "price"
        ]
        print("\nKeyword occurrence counts in rendered HTML:")
        for clue in clues:
            print(f"  {clue:10s}: {lower.count(clue)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
