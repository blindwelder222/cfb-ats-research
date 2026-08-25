#!/usr/bin/env python3
"""
BetMGM Selenium reconnaissance scraper v3.2.

Flow:
    1. Open the generic BetMGM football page.
    2. Discover the actual NCAAF navigation anchor from the rendered DOM.
    3. Follow that discovered href.
    4. Preserve the NCAAF page as raw evidence.
    5. Inventory event candidates and their surrounding DOM context.
    6. Capture date/time/week-like headings and event IDs/URLs.
    7. Preserve anonymous candidates separately.

This is reconnaissance code, not production acquisition code.
The workflow interface remains compatible with prior versions.
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
NCAAF_LABELS = {"ncaaf", "college football", "college-football"}
DATE_RE = re.compile(
    r"\b(?:"
    r"monday|tuesday|wednesday|thursday|friday|saturday|sunday"
    r")(?:,\s+[a-z]+\s+\d{1,2})?"
    r"|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
    r"[a-z]*\s+\d{1,2}"
    r"(?:,\s+\d{4})?",
    re.IGNORECASE,
)
TIME_RE = re.compile(
    r"\b(?:1[0-2]|0?[1-9])(?::[0-5]\d)?\s*(?:am|pm)\b",
    re.IGNORECASE,
)


def clean_text(value):
    return re.sub(r"\s+", " ", (value or "")).strip()


def extract_event_id(url):
    if not url:
        return None
    match = re.search(r":(\d+)(?:[/?#]|$)", url)
    return match.group(1) if match else None


def safe_filename(value):
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value[:100].strip("_") or "betmgm"


def element_context(element, depth=4):
    """Capture ancestor context without assuming a fixed component tree."""
    context = []
    current = element

    for level in range(depth + 1):
        try:
            tag = current.tag_name
            text = clean_text(current.text)
            classes = current.get_attribute("class")
            element_id = current.get_attribute("id")
            role = current.get_attribute("role")
            testid = current.get_attribute("data-testid")

            context.append(
                {
                    "level": level,
                    "tag": tag,
                    "text": text[:2000],
                    "class": classes,
                    "id": element_id,
                    "role": role,
                    "data-testid": testid,
                }
            )

            current = current.find_element(By.XPATH, "..")
        except Exception:
            break

    return context


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

    # Prefer a visible exact NCAAF anchor.
    for candidate in candidates:
        if candidate["visible"]:
            return candidate, candidates

    return (candidates[0] if candidates else None), candidates


def extract_event_record(event, selector):
    event_html = event.get_attribute("outerHTML") or ""
    event_text = clean_text(event.text)

    hrefs = []
    for anchor in event.find_elements(By.TAG_NAME, "a"):
        href = anchor.get_attribute("href")
        if href:
            hrefs.append(href)

    event_url = next(
        (href for href in hrefs if "/sports/events/" in href),
        None,
    )
    event_id = extract_event_id(event_url)

    # Search the event text for explicit date/time clues.
    date_matches = DATE_RE.findall(event_text)
    time_matches = TIME_RE.findall(event_text)

    return {
        "event_id": event_id,
        "event_url": event_url,
        "event_text": event_text[:5000],
        "event_text_date_clues": date_matches,
        "event_text_time_clues": time_matches,
        "html_length": len(event_html),
        "selector": selector,
        "ancestor_context": element_context(event, depth=4),
    }


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
        # Phase 1: discover NCAAF navigation target.
        # ---------------------------------------------------------------
        print(f"Opening football page: {initial_url}")
        driver.get(initial_url)
        time.sleep(wait_seconds)

        ncaaf_candidate, all_ncaaf_candidates = discover_ncaaf_href(driver)

        if not ncaaf_candidate:
            raise RuntimeError(
                "Could not discover a visible NCAAF anchor on the rendered "
                "football page."
            )

        discovered_href = ncaaf_candidate["href"]

        print(f"Discovered NCAAF href: {discovered_href}")

        navigation = {
            "initial_url": initial_url,
            "discovered_ncaaf": ncaaf_candidate,
            "all_ncaaf_candidates": all_ncaaf_candidates,
            "discovered_at_utc": datetime.now(timezone.utc).isoformat(),
        }

        # ---------------------------------------------------------------
        # Phase 2: follow the discovered route.
        # ---------------------------------------------------------------
        driver.get(discovered_href)

        print(f"Waiting {wait_seconds} seconds on NCAAF page...")
        time.sleep(wait_seconds)

        ncaaf_html = driver.page_source
        ncaaf_body = clean_text(
            driver.find_element(By.TAG_NAME, "body").text
        )

        prefix = output_dir / f"betmgm_ncaaf_probe_{stamp}"

        prefix.with_suffix(".html").write_text(
            ncaaf_html, encoding="utf-8"
        )
        prefix.with_suffix(".txt").write_text(
            ncaaf_body, encoding="utf-8"
        )
        driver.save_screenshot(str(prefix.with_suffix(".png")))

        # ---------------------------------------------------------------
        # Phase 3: event discovery.
        # ---------------------------------------------------------------
        selectors = [
            "div.grid-event-wrapper",
            "[class*='grid-event-wrapper']",
            "ms-event-detail",
        ]

        events_by_key = {}
        anonymous_candidates = []

        for selector in selectors:
            print(f"Checking selector: {selector}")

            for event in driver.find_elements(By.CSS_SELECTOR, selector):
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
                        anonymous_candidates.append(record)

                except Exception as exc:
                    print(f"Event extraction warning: {exc}")

        events = list(events_by_key.values())

        # ---------------------------------------------------------------
        # Phase 4: page-level structural clues.
        # ---------------------------------------------------------------
        headings = []
        for tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            for element in driver.find_elements(By.TAG_NAME, tag):
                try:
                    text = clean_text(element.text)
                    if text:
                        headings.append(
                            {
                                "tag": tag,
                                "text": text,
                                "context": element_context(element, depth=3),
                            }
                        )
                except Exception:
                    pass

        # Capture common text-bearing elements that look like date/week
        # group headers, without assuming the exact CSS/component structure.
        grouping_clues = []
        group_patterns = (
            "week ",
            "saturday",
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "august",
            "september",
            "october",
            "november",
            "december",
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
        )

        for element in driver.find_elements(
            By.CSS_SELECTOR,
            "div,span,p,li"
        ):
            try:
                text = clean_text(element.text)
                if not text or len(text) > 250:
                    continue

                low = text.lower()
                if any(pattern in low for pattern in group_patterns):
                    grouping_clues.append(
                        {
                            "tag": element.tag_name,
                            "text": text,
                            "class": element.get_attribute("class"),
                            "id": element.get_attribute("id"),
                            "role": element.get_attribute("role"),
                            "data-testid": element.get_attribute(
                                "data-testid"
                            ),
                            "context": element_context(element, depth=2),
                        }
                    )
            except Exception:
                pass

        # De-duplicate grouping clues by their most useful visible identity.
        unique_grouping = []
        seen_grouping = set()

        for clue in grouping_clues:
            signature = (
                clue["tag"],
                clue["text"],
                clue.get("class"),
                clue.get("id"),
            )
            if signature in seen_grouping:
                continue
            seen_grouping.add(signature)
            unique_grouping.append(clue)

        result = {
            "schema_version": "betmgm_probe_v3_2_ncaaf_structure",
            "retrieved_at_utc": timestamp.isoformat(),
            "sport_target": "NCAAF",
            "navigation": navigation,
            "page": {
                "final_url": driver.current_url,
                "page_title": driver.title,
                "html_bytes": len(ncaaf_html.encode("utf-8")),
                "body_text_chars": len(ncaaf_body),
            },
            "counts": {
                "unique_events": len(events),
                "anonymous_candidates": len(anonymous_candidates),
                "headings": len(headings),
                "grouping_clues": len(unique_grouping),
            },
            "events": events,
            "anonymous_candidates": anonymous_candidates,
            "headings": headings,
            "grouping_clues": unique_grouping,
        }

        json_path = (
            output_dir / f"betmgm_ncaaf_structure_{stamp}.json"
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
            "discovered_ncaaf_href": discovered_href,
            "final_url": driver.current_url,
            "page_title": driver.title,
            "wait_seconds": wait_seconds,
            "html_bytes": len(ncaaf_html.encode("utf-8")),
            "body_text_chars": len(ncaaf_body),
            "unique_event_count": len(events),
            "anonymous_candidate_count": len(anonymous_candidates),
            "heading_count": len(headings),
            "grouping_clue_count": len(unique_grouping),
        }

        metadata_path = (
            output_dir / f"betmgm_ncaaf_probe_{stamp}_metadata.json"
        )
        metadata_path.write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

        print("\n=== BetMGM NCAAF structure probe v3.2 complete ===")
        print(json.dumps(metadata, indent=2))

        print("\n=== First event records ===")
        for event in events[:25]:
            print(
                f"- {event['event_id']} | "
                f"{event['event_url']} | "
                f"{event['event_text'][:180]}"
            )

        print(f"\nFull structure artifact: {json_path}")
        print(f"Metadata: {metadata_path}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
