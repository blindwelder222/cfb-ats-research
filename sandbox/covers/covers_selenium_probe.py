#!/usr/bin/env python3
"""Covers NCAAF Selenium reconnaissance probe v1."""
import json, os, re, time
from datetime import datetime, timezone
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

DEFAULT_URL = "https://www.covers.com/sports/ncaaf/matchups"
KEYWORDS = ("calendar","season","week","ncaaf","college football","odds","weather","matchup")
ATTRS = ("href","aria-label","aria-labelledby","role","title","value","name","id","class",
         "data-testid","data-value","data-season","data-week","data-date","data-url","routerlink")

def clean(v): return re.sub(r"\s+", " ", (v or "")).strip()
def visible(e):
    try: return bool(e.is_displayed())
    except Exception: return False

def record(e):
    r={"tag":e.tag_name,"text":clean(e.text),"visible":visible(e)}
    for a in ATTRS:
        try:
            v=e.get_attribute(a)
            if v not in (None,""): r[a]=v
        except Exception: pass
    return r

def matches(r):
    s=" ".join(str(v) for k,v in r.items() if k!="visible").lower()
    return [k for k in KEYWORDS if k in s]

def main():
    url=os.getenv("COVERS_URL",DEFAULT_URL)
    wait=float(os.getenv("WAIT_SECONDS","8"))
    out=Path(os.getenv("OUTPUT_DIR","output")); out.mkdir(parents=True,exist_ok=True)
    ts=datetime.now(timezone.utc); stamp=ts.strftime("%Y%m%dT%H%M%SZ")
    o=Options()
    for arg in ("--headless=new","--no-sandbox","--disable-dev-shm-usage","--window-size=1920,1080","--disable-gpu"):
        o.add_argument(arg)
    driver=webdriver.Chrome(options=o)
    try:
        print(f"Opening Covers: {url}")
        driver.get(url); time.sleep(wait)
        html=driver.page_source
        body=clean(driver.find_element(By.TAG_NAME,"body").text)
        prefix=out/f"covers_probe_{stamp}"
        prefix.with_suffix(".html").write_text(html,encoding="utf-8")
        prefix.with_suffix(".txt").write_text(body,encoding="utf-8")
        driver.save_screenshot(str(prefix.with_suffix(".png")))

        anchors=[record(e) for e in driver.find_elements(By.TAG_NAME,"a")]
        buttons=[record(e) for e in driver.find_elements(By.TAG_NAME,"button")]
        selects=[record(e) for e in driver.find_elements(By.TAG_NAME,"select")]
        inputs=[record(e) for e in driver.find_elements(By.TAG_NAME,"input")]
        roles=[]
        for role in ("button","link","tab","combobox","listbox","option"):
            for e in driver.find_elements(By.CSS_SELECTOR,f'[role="{role}"]'):
                roles.append(record(e))

        cal=[]; seen=set()
        selectors=("[class*='calendar']","[class*='datepicker']","[class*='date-picker']",
                   "[class*='season']","[class*='week']","[aria-label*='calendar' i]",
                   "[aria-label*='season' i]","[aria-label*='week' i]",
                   "[data-testid*='calendar' i]","[data-testid*='season' i]","[data-testid*='week' i]")
        for sel in selectors:
            for e in driver.find_elements(By.CSS_SELECTOR,sel):
                try: sig=(e.tag_name,e.get_attribute("outerHTML")[:1000])
                except Exception: sig=id(e)
                if sig not in seen:
                    seen.add(sig); cal.append(record(e))

        game_links=[]
        for e in anchors:
            low=f"{e.get('href','')} {e.get('text','')}".lower()
            if any(x in low for x in ("/matchup","/matchups","/game","/odds","/preview","line move","line moves")):
                game_links.append(e)

        hits=[]; seen=set()
        for source,items in (("anchor",anchors),("button",buttons),("select",selects),("input",inputs),
                             ("role",roles),("calendar",cal),("matchup_link",game_links)):
            for r in items:
                m=matches(r)
                if not m: continue
                sig=json.dumps(r,sort_keys=True,ensure_ascii=False)
                if sig in seen: continue
                seen.add(sig); hits.append({"source_type":source,"matched_keywords":m,"element":r})

        headings=[]
        for tag in ("h1","h2","h3","h4","h5","h6"):
            for e in driver.find_elements(By.TAG_NAME,tag):
                t=clean(e.text)
                if t: headings.append({"tag":tag,"text":t,"class":e.get_attribute("class"),"id":e.get_attribute("id")})

        result={"schema_version":"covers_ncaaf_probe_v1","retrieved_at_utc":ts.isoformat(),
                "requested_url":url,"final_url":driver.current_url,"page_title":driver.title,
                "wait_seconds":wait,"counts":{"anchors":len(anchors),"buttons":len(buttons),
                "selects":len(selects),"inputs":len(inputs),"role_elements":len(roles),
                "calendar_elements":len(cal),"matchup_links":len(game_links),
                "keyword_hits":len(hits),"headings":len(headings)},
                "keyword_hits":hits,"calendar_elements":cal,"matchup_links":game_links,
                "anchors":anchors,"buttons":buttons,"selects":selects,"inputs":inputs,
                "role_elements":roles,"headings":headings}
        jp=out/f"covers_ncaaf_navigation_{stamp}.json"
        jp.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
        meta={"retrieved_at_utc":ts.isoformat(),"requested_url":url,"final_url":driver.current_url,
              "page_title":driver.title,"wait_seconds":wait,"html_bytes":len(html.encode()),
              "body_text_chars":len(body),"counts":result["counts"]}
        mp=out/f"covers_probe_{stamp}_metadata.json"
        mp.write_text(json.dumps(meta,indent=2),encoding="utf-8")
        print(json.dumps(meta,indent=2))
        print(f"\nFull navigation artifact: {jp}")
    finally:
        driver.quit()

if __name__=="__main__": main()
