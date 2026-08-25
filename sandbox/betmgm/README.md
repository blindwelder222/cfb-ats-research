# BetMGM Selenium Probe

Primitive reconnaissance tooling for the CFB ATS Research project.

## Purpose

This does **not** attempt to build the final BetMGM scraper.

It opens a public BetMGM sportsbook page in headless Chromium, gives the page time to execute JavaScript, and preserves the resulting artifacts so we can determine where the useful data actually lives.

The current probe saves:

- rendered HTML
- visible body text
- links
- a basic inventory of elements/classes/data-testid attributes
- page metadata
- screenshot
- simple keyword occurrence counts

## Local use

```bash
pip install -r requirements.txt
python betmgm_selenium_probe.py
```

Override the page:

```bash
BETMGM_URL="https://www.betmgm.com/en/sports/football-11" python betmgm_selenium_probe.py
```

## GitHub Actions

Run:

**Actions → BetMGM Selenium Probe → Run workflow**

The workflow allows the BetMGM URL and JavaScript wait time to be changed without editing the Python file.

The resulting files are uploaded as a workflow artifact named:

`betmgm-selenium-probe`

## What we are looking for

The first pass is intentionally exploratory.

After examining the artifacts, we can determine whether the useful betting data is:

1. directly present in the rendered DOM;
2. embedded as JSON in the page;
3. loaded through a network/API request; or
4. generated through another client-side mechanism.

If we find a clean underlying JSON endpoint, the next version should preferably use direct HTTP requests rather than Selenium for acquisition.

## Scope

This tool only reads a publicly accessible page. It does not log in, place bets, interact with a bet slip, or attempt to bypass access controls.
