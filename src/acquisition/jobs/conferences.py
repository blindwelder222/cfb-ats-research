import json
import os
from pathlib import Path

import cfbd


def main():

    print("===================================================")
    print("College Football ATS Research Platform")
    print("Conference Acquisition")
    print("===================================================")

    api_key = os.getenv("CFBD_API_KEY")

    if not api_key:
        raise RuntimeError("CFBD_API_KEY environment variable not found.")

    configuration = cfbd.Configuration(
        access_token=api_key
    )

    client = cfbd.ApiClient(configuration)

    api = cfbd.ConferencesApi(client)

    print("Downloading conferences...")

    conferences = api.get_conferences()

    output_dir = Path("data/raw/reference")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "conferences.json"

    with output_file.open("w", encoding="utf-8") as f:

        json.dump(
            [
                conference.to_dict()
                if hasattr(conference, "to_dict")
                else conference
                for conference in conferences
            ],
            f,
            indent=2,
            default=str
        )

    print(f"✓ conferences.json ({len(conferences)} conferences)")
    print("Done.")


if __name__ == "__main__":
    main()
