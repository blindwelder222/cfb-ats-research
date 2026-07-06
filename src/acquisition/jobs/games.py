import argparse
import json
import os
from pathlib import Path

import cfbd


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--season",
        required=True,
        type=int,
        help="Season to acquire"
    )

    args = parser.parse_args()

    print("===================================")
    print("CFBD Games Acquisition")
    print("===================================")

    api_key = os.getenv("CFBD_API_KEY")

    if not api_key:
        raise RuntimeError("CFBD_API_KEY was not found.")

    print("API key located.")

    configuration = cfbd.Configuration(
        access_token=api_key
    )

    client = cfbd.ApiClient(configuration)

    api = cfbd.GamesApi(client)

    print(f"Requesting season {args.season}...")

    games = api.get_games(
        year=args.season,
        classification="fbs"
    )

    print(f"Retrieved {len(games)} games.")

    output_dir = Path(f"data/raw/games/{args.season}")

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "games.json"

    with output_file.open("w", encoding="utf-8") as f:

        json.dump(
            [
                g.to_dict() if hasattr(g, "to_dict") else g
                for g in games
            ],
            f,
            indent=2,
            default=str
        )

    print(f"Archive written to {output_file}")

    print("Done.")


if __name__ == "__main__":
    main()
