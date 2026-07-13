import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

YEARS = range(2016, 2026)

INPUT_REGULAR = Path("data/normalized/games/regular")
INPUT_POST = Path("data/normalized/games/post")
OUTPUT_DIR = Path("data/normalized/seasons")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------

for year in YEARS:

    regular = pd.read_csv(
        INPUT_REGULAR / f"{year}_regular.csv"
    )

    postseason = pd.read_csv(
        INPUT_POST / f"{year}_post.csv"
    )

    season = pd.concat(
        [regular, postseason],
        ignore_index=True
    )

    season = season.sort_values(
        by="start_date"
    )

    output = OUTPUT_DIR / f"{year}_games.csv"

    season.to_csv(
        output,
        index=False
    )

    print("--------------------------------------------")
    print(f"{year}")
    print(f"Regular   : {len(regular)}")
    print(f"Post      : {len(postseason)}")
    print(f"Merged    : {len(season)}")

    expected = len(regular) + len(postseason)

    if len(season) != expected:
        raise RuntimeError(
            f"{year} record count mismatch."
        )

    print("PASS")

print("============================================")
print("Season Merge Complete")
print("============================================")
