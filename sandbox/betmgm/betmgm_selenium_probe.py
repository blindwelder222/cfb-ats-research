#!/usr/bin/env python3
"""
BetMGM Selenium reconnaissance scraper v3.3.

Goals:
    1. Discover the real NCAAF route from the rendered football page.
    2. Extract event URLs and numeric BetMGM event IDs.
    3. Extract event date/time clues.
    4. Detect and optionally click "More Events".
    5. Re-scan only the event selectors after expansion.
    6. Preserve raw evidence and concise diagnostics.

This is reconnaissance code, not production acquisition code.
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
from selenium.webdriver.support.ui import WebDriverWait


DEFAULT_URL = "https://www.betmgm.com/en/sports/football-11"
NCAAF_LABELS = {"ncaaf", "college football", "college-football"}

EVENT_SELECTORS = (
    "div.grid-event-wrapper",
    "[class*='grid-event-wrapper']",
    "ms-event-detail",
)

DATE_RE = re.compile(
    r"\b(?:"
    r"(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
    r"(?:,\s+[a-z]+\s+\d{1,2})?"
    r"|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
    r"[a-z]*\s+\d{1,2}"
    r"(?:,\s+\d{4})?"
    r"|(?:\d{1,2}/\d{1,2}/\d{2,4})"
    r")",
    re.IGNORECASE,
)

TIME_RE = re.compile(
    r"\b(?:1[0-2]|0?[1-9])(?::[0-5]\d)?\s*(?:am|pm)\b",
    re.IGNORECASE,
)

EVENT_ID_PATTERNS = (
    re.compile(r":(\d+)(?:[/?#]|$)"),
    re.compile(r"-(\d+)(?:[/?#]|$)"),
)


def clean_text(value):
    return re.sub(r"\s+", " ", (value or "")).strip()


def extract_event_id(url):
    if not url:
        return None

    for pattern in EVENT_ID_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)

    return None


def discover_ncaaf_href(driver):
    candidates = []

    for anchor in driver.find_elements(By.TAG_NAME, "a"):
        try:
            text = clean_text(anchor.text)
            href = anchor.get_attribute("href")

            if text.lower() in NCAAF_LABELS and href:
                candidates.append(
                    {
                        "text": text,
                        "href": href,
                        "visible": anchor.is_displayed(),
                        "class": anchor.get_attribute("class"),
                        "data-testid": anchor.get_attribute("data-testid"),
                        "aria-label": anchor.get_attribute("aria-label"),
                    }
                )
        except Exception:
            pass

    for candidate in candidates:
        if candidate["visible"]:
            return candidate, candidates

    return (candidates[0] if candidates else None), candidates


def find_event_url(event):
    for anchor in event.find_elements(By.TAG_NAME, "a"):
        try:
            href = anchor.get_attribute("href")
            if href and "/sports/events/" in href:
                return href
        except Exception:
            pass

    return None


def extract_event_record(event, selector):
    event_url = find_event_url(event)
    event_id = extract_event_id(event_url)
    event_text = clean_text(event.text)

    date_clues = DATE_RE.findall(event_text)
    time_clues = TIME_RE.findall(event_text)

    return {
        "event_id": event_id,
        "event_url": event_url,
        "event_text": event_text[:5000],
        "date_clues": date_clues,
        "time_clues": time_clues,
        "selector": selector,
    }


def collect_events(driver):
    events_by_key = {}
    anonymous = []

    for selector in EVENT_SELECTORS:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)

        for event in elements:
            try:
                record = extract_event_record(event, selector)
                event_id = record["event_id"]
                event_url = record["event_url"]
                event_text = record["event_text"]

                if event_id:
                    key = f"id:{event_id}"
                elif event_url:
                    key = f"url:{event_url}"
                else:
                    key = None

                if key:
                    if key not in events_by_key:
                        events_by_key[key] = record
                elif event_text:
                    anonymous.append(record)

            except Exception as exc:
                print(f"Event extraction warning: {exc}")

    return list(events_by_key.values()), anonymous


def find_more_events(driver):
    candidates = []

    # Keep this targeted. Avoid scanning the entire DOM tree.
    selectors = (
        "button",
        "a",
        '[role="button"]',
        '[role="link"]',
    )

    seen = set()

    for selector in selectors:
        for element in driver.find_elements(By.CSS_SELECTOR, selector):
            try:
                text = clean_text(element.text)
                aria = clean_text(element.get_attribute("aria-label"))

                combined = f"{text} {aria}".lower()

                if "more event" not in combined:
                    continue

                signature = (
                    element.tag_name,
                    text,
                    aria,
                    element.get_attribute("class"),
                )

                if signature in seen:
                    continue

                seen.add(signature)

                candidates.append(
                    {
                        "tag": element.tag_name,
                        "text": text,
                        "aria-label": aria,
                        "visible": element.is_displayed(),
                        "enabled": element.is_enabled(),
                        "class": element.get_attribute("class"),
                        "id": element.get_attribute("id"),
                    }
                )
            except Exception:
                pass

    return candidates


def click_more_events(driver, candidates):
    for candidate in candidates:
        if not candidate["visible"] or not candidate["enabled"]:
            continue

        # Re-find by text/aria rather than retaining a stale WebElement.
        xpath_candidates = [
            (
                By.XPATH,
                "//button[contains("
                "translate(normalize-space(.), "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), "
                "'more events')]"
            ),
            (
                By.XPATH,
                "//a[contains("
                "translate(normalize-space(.), "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), "
                "'more events')]"
            ),
            (
                By.XPATH,
                "//*[@role='button' and contains("
                "translate(normalize-space(.), "
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
                "'abcdefghijklmnopqrstuvwxyz'), "
                "'more events')]"
            ),
        ]

        for by, locator in xpath_candidates:
            try:
                elements = driver.find_elements(by, locator)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center'});",
                            element,
                        )
                        time.sleep(0.5)
                        driver.execute_script(
                            "arguments[0].click();",
                            element,
                        )
                        return True
            except Exception as exc:
                print(f"More Events click attempt: {exc}")

    return False


def main():
    initial_url = os.getenv("BETMGM_URL", DEFAULT_URL)
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
        # ---------------------------------------------------------------
        # Phase 1: discover NCAAF route.
        # ---------------------------------------------------------------
        print(f"Opening football page: {initial_url}")
        driver.get(initial_url)
        time.sleep(wait_seconds)

        ncaaf_candidate, all_ncaaf_candidates = discover_ncaaf_href(driver)

        if not ncaaf_candidate:
            raise RuntimeError(
                "Could not discover a visible NCAAF anchor."
            )

        ncaaf_href = ncaaf_candidate["href"]
        print(f"Discovered NCAAF href: {ncaaf_href}")

        # ---------------------------------------------------------------
        # Phase 2: navigate to NCAAF.
        # ---------------------------------------------------------------
        driver.get(ncaaf_href)
        time.sleep(wait_seconds)

        initial_ncaaf_url = driver.current_url
        initial_ncaaf_title = driver.title

        # ---------------------------------------------------------------
        # Phase 3: collect initial event set.
        # ---------------------------------------------------------------
        initial_events, initial_anonymous = collect_events(driver)
        more_candidates_before = find_more_events(driver)

        print(
            f"Initial unique events: {len(initial_events)} | "
            f"anonymous: {len(initial_anonymous)} | "
            f"More Events controls: {len(more_candidates_before)}"
        )

        # ---------------------------------------------------------------
        # Phase 4: attempt one More Events expansion.
        # ---------------------------------------------------------------
        clicked_more = False
        if more_candidates_before:
            clicked_more = click_more_events(
                driver,
                more_candidates_before,
            )

            if clicked_more:
                # Give the client-side list a short, bounded period to grow.
                time.sleep(3)

        after_events, after_anonymous = collect_events(driver)
        more_candidates_after = find_more_events(driver)

        new_ids = sorted(
            {
                event["event_id"]
                for event in after_events
                if event["event_id"]
            }
            -
            {
                event["event_id"]
                for event in initial_events
                if event["event_id"]
            }
        )

        # ---------------------------------------------------------------
        # Phase 5: preserve final raw evidence.
        # ---------------------------------------------------------------
        final_html = driver.page_source
        final_body = clean_text(
            driver.find_element(By.TAG_NAME, "body").text
        )

        prefix = output_dir / f"betmgm_ncaaf_v33_{stamp}"

        prefix.with_suffix(".html").write_text(
            final_html, encoding="utf-8"
        )
        prefix.with_suffix(".txt").write_text(
            final_body, encoding="utf-8"
        )
        driver.save_screenshot(str(prefix.with_suffix(".png")))

        result = {
            "schema_version": "betmgm_probe_v3_3_ncaaf_events",
            "retrieved_at_utc": timestamp.isoformat(),
            "navigation": {
                "initial_url": initial_url,
                "discovered_ncaaf": ncaaf_candidate,
                "all_ncaaf_candidates": all_ncaaf_candidates,
                "final_url": driver.current_url,
                "page_title": driver.title,
            },
            "initial_state": {
                "unique_event_count": len(initial_events),
                "anonymous_candidate_count": len(initial_anonymous),
                "more_events_candidates": more_candidates_before,
                "events": initial_events,
            },
            "more_events_test": {
                "clicked": clicked_more,
                "new_unique_event_count": len(after_events)
                - len(initial_events),
                "new_event_ids": new_ids,
                "more_events_candidates_after": more_candidates_after,
            },
            "final_state": {
                "unique_event_count": len(after_events),
                "anonymous_candidate_count": len(after_anonymous),
                "events": after_events,
            },
        }

        json_path = (
            output_dir / f"betmgm_ncaaf_events_v33_{stamp}.json"
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
            "initial_url": initial_url,
            "discovered_ncaaf_href": ncaaf_href,
            "initial_ncaaf_url": initial_ncaaf_url,
            "final_url": driver.current_url,
            "page_title": driver.title,
            "initial_unique_event_count": len(initial_events),
            "initial_anonymous_count": len(initial_anonymous),
            "more_events_candidate_count": len(
                more_candidates_before
            ),
            "more_events_clicked": clicked_more,
            "final_unique_event_count": len(after_events),
            "final_anonymous_count": len(after_anonymous),
            "new_event_count": len(new_ids),
            "new_event_ids": new_ids,
            "final_html_bytes": len(
                final_html.encode("utf-8")
            ),
            "final_body_text_chars": len(final_body),
        }

        metadata_path = (
            output_dir / f"betmgm_ncaaf_v33_{stamp}_metadata.json"
        )
        metadata_path.write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

        print("\n=== BetMGM NCAAF V3.3 complete ===")
        print(json.dumps(metadata, indent=2))

        print("\n=== Initial event IDs ===")
        for event in initial_events:
            print(
                f"- {event['event_id']} | "
                f"{event['event_url']} | "
                f"{event['event_text'][:160]}"
            )

        print(f"\nFull artifact: {json_path}")
        print(f"Metadata: {metadata_path}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
