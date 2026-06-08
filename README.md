# premier-league-analytics

Multi-season Premier League performance analytics covering team and player statistics, correlation analysis, statistical significance testing, and player similarity scoring.

## What's Inside

Three staged notebooks:

| Notebook | Focus |
|---|---|
| `01_data_acquisition.ipynb` | Fetch 2022-23 and 2023-24 season data, clean and join |
| `02_team_analysis.ipynb` | League table trends, correlation heatmap, ranked bar charts |
| `03_player_analysis.ipynb` | Radar charts, scatter + regression, player similarity |

## Quick Start

```bash
pip install -r requirements.txt
python data/fetch_data.py   # downloads two seasons of match CSVs (no auth)
jupyter lab
```

The committed notebooks are already executed against real data, so all charts
render on GitHub.

## Data Source

[football-data.co.uk](https://www.football-data.co.uk/englandm.php) — free match
statistics CSVs, no authentication required. Two seasons (760 matches) are fetched:

- `data/E0_2223.csv` — Premier League 2022-23
- `data/E0_2324.csv` — Premier League 2023-24

Team-level season tables are aggregated from these match results. The player
analysis uses an embedded **representative per-90 sample** of leading 2023-24
players (so the radar/similarity demo is fully reproducible without scraping);
swap in a `soccerdata`/FBref pull for the full squad if desired. Raw CSVs are git-ignored.

## Selected Figures

![Correlation heatmap](outputs/figures/correlation_heatmap.png)

![Player radar](outputs/figures/player_radar.png)

## Player Similarity

`src/similarity.py` implements `find_similar_players(df, player_name, n, metric)` which returns the *n* most similar players using Euclidean or cosine distance on a configurable set of per-90 metrics.

```python
from src.similarity import find_similar_players
find_similar_players(player_stats, "Erling Haaland", n=5, metric="cosine")
```

## Key Artefacts

| File | Description |
|---|---|
| `outputs/figures/correlation_heatmap.png` | 10+ metric correlation matrix |
| `outputs/figures/player_radar.png` | Per-90 radar for selected players |

## Project Structure

```
premier-league-analytics/
├── data/
│   ├── fetch_data.py
│   └── README.md
├── notebooks/
│   ├── 01_data_acquisition.ipynb
│   ├── 02_team_analysis.ipynb
│   └── 03_player_analysis.ipynb
├── outputs/
│   └── figures/
├── src/
│   ├── similarity.py
│   └── charts.py
├── tests/
│   └── test_similarity.py
├── requirements.txt
└── pyproject.toml
```

## Licence

Code: MIT. Data: football-data.co.uk (free for non-commercial use).
