# Data

`python data/fetch_data.py` downloads two files from [football-data.co.uk](https://www.football-data.co.uk/englandm.php) (free for non-commercial use). They are git-ignored.

- `E0_2223.csv`: 2022-23 season, 380 matches
- `E0_2324.csv`: 2023-24 season, 380 matches

Columns used: `HomeTeam`, `AwayTeam`, `FTHG`/`FTAG` (goals), `FTR` (result), `HS`/`AS` (shots), `HST`/`AST` (shots on target), `HC`/`AC` (corners), `HY`/`AY` and `HR`/`AR` (cards).
