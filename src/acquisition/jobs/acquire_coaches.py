"""
Acquire the canonical CFBD coach reference dataset.

The /coaches endpoint is a parameterless reference endpoint. It returns
coach identity information plus season-by-season coaching history and
statistics. The raw API response is preserved as JSON and is not flattened
or otherwise transformed at this stage.

Output:
    data/raw/coaches/coaches.json
"""

import json
import os
from pathlib import Path

import cfbd


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

OUTPUT_DIR = Path("data/raw/coaches")
OUTPUT_FILE = OUTPUT_DIR / "coaches.json"


# ---------------------------------------------------------------------
# Acquisition
# ---------------------------------------------------------------------

def acquire_coaches(api):
    """Download the complete CFBD coach reference dataset."""
    print("Downloading coach reference data...")

    coaches = api.get_coaches()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as output_file:
        json.dump(
            [
                coach.to_dict() if hasattr(coach, "to_dict") else coach
                for coach in coaches
            ],
            output_file,
            indent=2,
            default=str,
        )

    print(f"  ✓ {OUTPUT_FILE} ({len(coaches)} coaches)")

    return len(coaches)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    print("===================================================")
    print("College Football ATS Research Platform")
    print("Coach Reference Acquisition")
    print("===================================================")

    api_key = os.getenv("CFBD_API_KEY")

    if not api_key:
        raise RuntimeError(
            "CFBD_API_KEY environment variable not found."
        )

    configuration = cfbd.Configuration(
        access_token=api_key
    )

    client = cfbd.ApiClient(configuration)
    api = cfbd.CoachesApi(client)

    total_coaches = acquire_coaches(api)

    print()
    print("===================================================")
    print("Coach Reference Acquisition Complete")
    print("===================================================")
    print(f"Coaches Retrieved: {total_coaches:,}")
    print(f"Output File      : {OUTPUT_FILE}")
    print("API Calls Used   : 1")
    print("===================================================")


if __name__ == "__main__":
    main()
