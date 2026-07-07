import json
import os
from pathlib import Path

import cfbd


def main():

    print("===================================================")
    print("College Football ATS Research Platform")
    print("Venue Acquisition")
    print("===================================================")

    api_key = os.getenv("CFBD_API_KEY")

    if not api_key:
        raise RuntimeError("CFBD_API_KEY environment variable not found.")

    configuration = cfbd.Configuration(
        access_token=api_key
    )

    client = cfbd.ApiClient(configuration)

    api = cfbd.VenuesApi(client)

    print("Downloading venues...")

    venues = api.get_venues()

    output_dir = Path("data/raw/reference")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "venues.json"

    with output_file.open("w", encoding="utf-8") as f:

        json.dump(
            [
                venue.to_dict()
                if hasattr(venue, "to_dict")
                else venue
                for venue in venues
            ],
            f,
            indent=2,
            default=str
        )

    print(f"✓ venues.json ({len(venues)} venues)")
    print("Done.")


if __name__ == "__main__":
    main()
