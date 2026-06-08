"""Download Premier League match statistics from football-data.co.uk."""

import sys
from pathlib import Path

import requests

SEASONS = {
    "E0_2223.csv": "https://www.football-data.co.uk/mmz4281/2223/E0.csv",
    "E0_2324.csv": "https://www.football-data.co.uk/mmz4281/2324/E0.csv",
}

DATA_DIR = Path(__file__).parent


def download(url: str, dest: Path) -> None:
    if dest.exists():
        print(f"  already exists: {dest.name}")
        return
    print(f"  downloading {dest.name} …", end=" ", flush=True)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    dest.write_bytes(r.content)
    rows = len(r.text.splitlines()) - 1
    print(f"done ({rows} matches)")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading Premier League match data from football-data.co.uk…")
    for name, url in SEASONS.items():
        download(url, DATA_DIR / name)
    print("Done.")


if __name__ == "__main__":
    main()
