#!/usr/bin/env python3
"""
Covers NCAAF Selenium reconnaissance probe v2.

Controlled comparison:
    A) one matchup from the default/current NCAAF page
    B) LSU matchup from 2019-2020 Week 9

The script:
    - opens the current NCAAF matchup page;
    - finds a game-level Matchup link/button;
    - records its URL and numeric game ID;
    - opens that game page and inventories historical/current data;
    - opens the calendar;
    - discovers the 2019-2020 Week 9 href from the rendered DOM;
    - follows that href;
    - finds the LSU matchup;
    - records its game URL and numeric game ID;
    - opens the historical game page;
    - inventories odds, lists, weather, score, links, tables and visible text.

This is reconnaissance code. It intentionally preserves raw evidence and
does not yet attempt bulk historical acquisition.
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


DEFAULT_URL = "https://www.covers.com/sports/ncaaf/matchups"

EVENT_TERMS = (
    "matchup",
    "preview",
    "odds",
    "line moves",
    "line move",
    "trends",
)

ID_PATTERNS = (
    re.compile(r"[?&](?:id|gameid|game_id)=(\d+)", re.I),
    re.compile(r"(?:^|[-_/])(\d{4,})(?:[/?#]|$)"),
)

def clean(value):
    return re.sub(r"\s+", " ", (value or "")).strip()

def get_id(url):
    if not url:
        return None
    for pattern in ID_PATTERNS:
        m = pattern.search(url)
        if m:
            return m.group(1)
    return None

def attrs(element):
    result = {}
    for name in (
        "href", "aria-label", "title", "role", "id", "class",
        "data-testid", "data-game-id", "data-id", "data-url",
    ):
        try:
            value = element.get_attribute(name)
            if value not in (None, ""):
                result[name] = value
        except Exception:
            pass
    return result

def record_element(element, include_html=False):
    result = {
        "tag": element.tag_name,
        "text": clean(element.text),
        "attributes": attrs(element),
    }
    if include_html:
        try:
            result["outer_html"] = element.get_attribute("outerHTML")
        except Exception:
            pass
    return result

def visible(element):
    try:
        return element.is_displayed()
    except Exception:
        return False

def find_matchup_links(driver):
    results = []
    seen = set()

    for element in driver.find_elements(By.TAG_NAME, "a"):
        try:
            href = element.get_attribute("href") or ""
            text = clean(element.text)
            low = f"{href} {text}".lower()

            if not any(term in low for term in EVENT_TERMS):
                continue

            if not href:
                continue

            key = (href, text)
            if key in seen:
                continue
            seen.add(key)

            results.append({
                "text": text,
                "href": href,
                "game_id": get_id(href),
                "attributes": attrs(element),
                "visible": visible(element),
            })
        except Exception:
            pass

    return results

def choose_current_matchup(links):
    # Prefer a visible link whose label is exactly/mostly "Matchup".
    for item in links:
        if item["visible"] and item["text"].strip().lower() == "matchup":
            return item
    for item in links:
        if item["visible"]:
            return item
    return links[0] if links else None

def discover_calendar_week(driver, season_label="2019-2020", week_label="Week 9"):
    """
    Find the season and week anchors already rendered in the calendar.
    We do not guess a selectedDate. We inspect the actual href.
    """
    result = {
        "season_label": season_label,
        "week_label": week_label,
        "season_link": None,
        "week_link": None,
        "all_matching_week_links": [],
    }

    # Open the calendar if it exists.
    calendar_buttons = []
    for selector in (
        "#calendar-btn",
        "[id*='calendar-btn']",
        "[aria-label*='calendar' i]",
        "button[class*='calendar' i]",
    ):
        try:
            calendar_buttons.extend(
                driver.find_elements(By.CSS_SELECTOR, selector)
            )
        except Exception:
            pass

    opened = False
    for button in calendar_buttons:
        try:
            if visible(button):
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    button,
                )
                driver.execute_script("arguments[0].click();", button)
                time.sleep(1)
                opened = True
                break
        except Exception:
            pass

    result["calendar_opened"] = opened

    # Search anchors for the exact season.
    season_candidates = []
    for anchor in driver.find_elements(By.TAG_NAME, "a"):
        try:
            text = clean(anchor.text)
            href = anchor.get_attribute("href") or ""
            if text == season_label and href:
                season_candidates.append({
                    "text": text,
                    "href": href,
                    "attributes": attrs(anchor),
                    "visible": visible(anchor),
                })
        except Exception:
            pass

    if season_candidates:
        result["season_link"] = season_candidates[0]

    # Search for Week 9. If both current and historical week lists are
    # rendered, keep all candidates so we can see which date the site uses.
    for anchor in driver.find_elements(By.TAG_NAME, "a"):
        try:
            text = clean(anchor.text)
            href = anchor.get_attribute("href") or ""
            if text.lower().startswith(week_label.lower()) and href:
                item = {
                    "text": text,
                    "href": href,
                    "attributes": attrs(anchor),
                    "visible": visible(anchor),
                }
                result["all_matching_week_links"].append(item)
        except Exception:
            pass

    # Prefer a Week 9 link whose visible text contains a date range and
    # whose surrounding season list corresponds to 2019-2020. If the site
    # exposes only one Week 9, use it.
    if result["all_matching_week_links"]:
        result["week_link"] = result["all_matching_week_links"][0]

    return result

def find_lsu_matchup(driver):
    candidates = []

    # First use anchors with obvious matchup/game terms.
    for item in find_matchup_links(driver):
        low = item["text"].lower()
        if "lsu" in low:
            candidates.append(item)

    # Also inspect all anchors because the visible game link may be named
    # after the teams rather than "Matchup".
    if not candidates:
        for anchor in driver.find_elements(By.TAG_NAME, "a"):
            try:
                text = clean(anchor.text)
                href = anchor.get_attribute("href") or ""
                if "lsu" in text.lower() and href:
                    candidates.append({
                        "text": text,
                        "href": href,
                        "game_id": get_id(href),
                        "attributes": attrs(anchor),
                        "visible": visible(anchor),
                    })
            except Exception:
                pass

    # De-duplicate.
    unique = []
    seen = set()
    for item in candidates:
        key = item["href"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)

    return unique

def inventory_game_page(driver):
    """Capture broad evidence without assuming the final schema."""
    html = driver.page_source
    body = clean(driver.find_element(By.TAG_NAME, "body").text)

    lists = []
    for ul in driver.find_elements(By.TAG_NAME, "ul"):
        try:
            items = []
            for li in ul.find_elements(By.TAG_NAME, "li"):
                text = clean(li.text)
                if text:
                    items.append({
                        "text": text,
                        "html": li.get_attribute("outerHTML"),
                    })
            if items:
                lists.append({
                    "text": clean(ul.text)[:10000],
                    "items": items[:200],
                    "html": ul.get_attribute("outerHTML"),
                })
        except Exception:
            pass

    tables = []
    for table in driver.find_elements(By.TAG_NAME, "table"):
        try:
            tables.append({
                "text": clean(table.text)[:15000],
                "html": table.get_attribute("outerHTML"),
            })
        except Exception:
            pass

    headings = []
    for tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        for e in driver.find_elements(By.TAG_NAME, tag):
            text = clean(e.text)
            if text:
                headings.append({
                    "tag": tag,
                    "text": text,
                    "attributes": attrs(e),
                })

    weather_candidates = []
    for element in driver.find_elements(By.XPATH, "//*"):
        try:
            text = clean(element.text)
            if not text or len(text) > 500:
                continue
            low = text.lower()
            if any(term in low for term in (
                "weather", "temperature", "wind", "humidity",
                "precipitation", "forecast",
            )):
                weather_candidates.append({
                    "tag": element.tag_name,
                    "text": text,
                    "attributes": attrs(element),
                })
        except Exception:
            pass

    # De-duplicate weather snippets.
    weather_unique = []
    seen_weather = set()
    for item in weather_candidates:
        key = (item["tag"], item["text"], json.dumps(
            item["attributes"], sort_keys=True
        ))
        if key in seen_weather:
            continue
        seen_weather.add(key)
        weather_unique.append(item)

    odds_candidates = []
    for element in driver.find_elements(By.XPATH, "//*"):
        try:
            text = clean(element.text)
            if not text or len(text) > 700:
                continue
            low = text.lower()
            if any(term in low for term in (
                "spread", "moneyline", "total", "over", "under",
                "opening odds", "closing odds", "consensus",
                "line movement", "odds",
            )):
                odds_candidates.append({
                    "tag": element.tag_name,
                    "text": text,
                    "attributes": attrs(element),
                })
        except Exception:
            pass

    odds_unique = []
    seen_odds = set()
    for item in odds_candidates:
        key = (item["tag"], item["text"], json.dumps(
            item["attributes"], sort_keys=True
        ))
        if key in seen_odds:
            continue
        seen_odds.add(key)
        odds_unique.append(item)

    links = []
    for anchor in driver.find_elements(By.TAG_NAME, "a"):
        try:
            href = anchor.get_attribute("href") or ""
            text = clean(anchor.text)
            if href or text:
                links.append({
                    "text": text,
                    "href": href,
                    "game_id": get_id(href),
                    "attributes": attrs(anchor),
                })
        except Exception:
            pass

    return {
        "url": driver.current_url,
        "title": driver.title,
        "body_text": body,
        "body_text_chars": len(body),
        "html_bytes": len(html.encode("utf-8")),
        "headings": headings,
        "lists": lists,
        "tables": tables,
        "weather_candidates": weather_unique[:300],
        "odds_candidates": odds_unique[:500],
        "links": links,
        "raw_html": html,
    }

def save_page_evidence(driver, out_dir, prefix):
    html = driver.page_source
    body = clean(driver.find_element(By.TAG_NAME, "body").text)

    (out_dir / f"{prefix}.html").write_text(html, encoding="utf-8")
    (out_dir / f"{prefix}.txt").write_text(body, encoding="utf-8")
    driver.save_screenshot(str(out_dir / f"{prefix}.png"))

def open_url_and_wait(driver, url, wait_seconds):
    driver.get(url)
    time.sleep(wait_seconds)

def main():
    start_url = os.getenv("COVERS_URL", DEFAULT_URL)
    wait_seconds = float(os.getenv("WAIT_SECONDS", "8"))
    output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc)
    stamp = ts.strftime("%Y%m%dT%H%M%SZ")

    options = Options()
    for arg in (
        "--headless=new",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--window-size=1920,1080",
        "--disable-gpu",
    ):
        options.add_argument(arg)

    driver = webdriver.Chrome(options=options)

    try:
        result = {
            "schema_version": "covers_ncaaf_probe_v2_current_vs_2019_week9",
            "retrieved_at_utc": ts.isoformat(),
            "target": {
                "current_page": start_url,
                "historical_season": "2019-2020",
                "historical_week": "Week 9",
                "historical_team": "LSU",
            },
        }

        # ---------------------------------------------------------------
        # A. Current/default page
        # ---------------------------------------------------------------
        print(f"Opening current page: {start_url}")
        open_url_and_wait(driver, start_url, wait_seconds)

        current_links = find_matchup_links(driver)
        current_matchup = choose_current_matchup(current_links)

        result["current_page"] = {
            "url": driver.current_url,
            "title": driver.title,
            "candidate_links": current_links,
            "selected_matchup": current_matchup,
        }

        if not current_matchup:
            raise RuntimeError(
                "Could not find a game-level matchup link on the "
                "default Covers NCAAF page."
            )

        print(
            "Current matchup selected:",
            current_matchup["text"],
            current_matchup["href"],
            current_matchup["game_id"],
        )

        open_url_and_wait(
            driver,
            current_matchup["href"],
            wait_seconds,
        )

        save_page_evidence(
            driver,
            output_dir,
            f"current_game_{stamp}",
        )

        result["current_game"] = {
            "source_matchup": current_matchup,
            "inventory": inventory_game_page(driver),
        }

        # ---------------------------------------------------------------
        # B. Historical calendar -> 2019-2020 Week 9
        # ---------------------------------------------------------------
        print("\nReturning to current NCAAF page for calendar...")
        open_url_and_wait(driver, start_url, wait_seconds)

        calendar = discover_calendar_week(
            driver,
            season_label="2019-2020",
            week_label="Week 9",
        )

        result["calendar_discovery"] = calendar

        # V1 proved that Covers embeds the season/week navigation in the
        # rendered DOM even when the calendar UI is closed. Read the
        # canonical hrefs directly instead of trying to click a hidden
        # JavaScript control.
        season_url = None
        week_candidates = []

        for anchor in driver.find_elements(
            By.CSS_SELECTOR, "#season-list a"
        ):
            try:
                text = clean(anchor.text)
                href = anchor.get_attribute("href") or ""
                if text == "2019-2020" and href:
                    season_url = href
                    break
            except Exception:
                pass

        for anchor in driver.find_elements(
            By.CSS_SELECTOR, "#week-list a"
        ):
            try:
                text = clean(anchor.text)
                href = anchor.get_attribute("href") or ""
                if text.lower().startswith("week 9") and href:
                    week_candidates.append({
                        "text": text,
                        "href": href,
                        "attributes": attrs(anchor),
                    })
            except Exception:
                pass

        result["calendar_dom_navigation"] = {
            "season_2019_2020_href": season_url,
            "week_9_candidates": week_candidates,
        }

        if not week_candidates:
            raise RuntimeError(
                "Could not find a Week 9 link in the rendered "
                "#week-list."
            )

        # If multiple Week 9 links coexist, use the one whose
        # selectedDate belongs to calendar year 2019. This is based on
        # the actual hrefs exposed by Covers; no URL is fabricated.
        import urllib.parse

        def selected_date(href):
            try:
                query = urllib.parse.parse_qs(
                    urllib.parse.urlparse(href).query
                )
                return query.get("selectedDate", [None])[0]
            except Exception:
                return None

        dated_2019 = [
            item for item in week_candidates
            if (selected_date(item["href"]) or "").startswith("2019-")
        ]

        if len(dated_2019) == 1:
            historical_url = dated_2019[0]["href"]
        elif len(week_candidates) == 1:
            historical_url = week_candidates[0]["href"]
        else:
            raise RuntimeError(
                "Multiple Week 9 links were found, but the historical "
                "2019-2020 Week 9 link could not be identified from "
                "the rendered hrefs."
            )

        print("2019-2020 season href:", season_url)
        print("2019-2020 Week 9 href:", historical_url)

        open_url_and_wait(
            driver,
            historical_url,
            wait_seconds,
        )

        historical_links = find_matchup_links(driver)
        lsu_candidates = find_lsu_matchup(driver)

        result["historical_week_page"] = {
            "url": driver.current_url,
            "title": driver.title,
            "candidate_links": historical_links,
            "lsu_candidates": lsu_candidates,
        }

        if not lsu_candidates:
            raise RuntimeError(
                "Could not find an LSU matchup on the selected "
                "2019-2020 Week 9 page."
            )

        lsu_matchup = lsu_candidates[0]

        print(
            "LSU matchup selected:",
            lsu_matchup["text"],
            lsu_matchup["href"],
            lsu_matchup["game_id"],
        )

        open_url_and_wait(
            driver,
            lsu_matchup["href"],
            wait_seconds,
        )

        save_page_evidence(
            driver,
            output_dir,
            f"historical_lsu_2019_week9_{stamp}",
        )

        result["historical_lsu_game"] = {
            "source_matchup": lsu_matchup,
            "inventory": inventory_game_page(driver),
        }

        # ---------------------------------------------------------------
        # Summary
        # ---------------------------------------------------------------
        result["comparison"] = {
            "current_game_url": result["current_game"]["inventory"]["url"],
            "current_game_id": current_matchup["game_id"],
            "historical_week_url": historical_url,
            "historical_lsu_game_url": result["historical_lsu_game"]["inventory"]["url"],
            "historical_lsu_game_id": lsu_matchup["game_id"],
            "current_list_count": len(
                result["current_game"]["inventory"]["lists"]
            ),
            "historical_list_count": len(
                result["historical_lsu_game"]["inventory"]["lists"]
            ),
            "current_table_count": len(
                result["current_game"]["inventory"]["tables"]
            ),
            "historical_table_count": len(
                result["historical_lsu_game"]["inventory"]["tables"]
            ),
            "current_weather_candidate_count": len(
                result["current_game"]["inventory"]["weather_candidates"]
            ),
            "historical_weather_candidate_count": len(
                result["historical_lsu_game"]["inventory"]["weather_candidates"]
            ),
            "current_odds_candidate_count": len(
                result["current_game"]["inventory"]["odds_candidates"]
            ),
            "historical_odds_candidate_count": len(
                result["historical_lsu_game"]["inventory"]["odds_candidates"]
            ),
        }

        json_path = (
            output_dir /
            f"covers_ncaaf_v2_current_vs_2019_week9_{stamp}.json"
        )
        json_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        metadata = {
            "retrieved_at_utc": ts.isoformat(),
            "current_game_id": current_matchup["game_id"],
            "current_game_url": result["current_game"]["inventory"]["url"],
            "historical_week_url": historical_url,
            "historical_lsu_game_id": lsu_matchup["game_id"],
            "historical_lsu_game_url": result["historical_lsu_game"]["inventory"]["url"],
            "comparison": result["comparison"],
        }

        metadata_path = (
            output_dir /
            f"covers_ncaaf_v2_{stamp}_metadata.json"
        )
        metadata_path.write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8",
        )

        print("\n=== Covers NCAAF V2 complete ===")
        print(json.dumps(metadata, indent=2))
        print("\nPrimary artifact:", json_path)
        print("Metadata:", metadata_path)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
