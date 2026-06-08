# Dataset Provenance

**Source**: football-data.co.uk — Premier League match statistics  
**URL**: https://www.football-data.co.uk/englandm.php  
**Licence**: Free for non-commercial use  

## Files

| File | Season | Matches |
|---|---|---|
| `E0_2223.csv` | 2022-23 Premier League | 380 |
| `E0_2324.csv` | 2023-24 Premier League | 380 |

Raw CSVs are git-ignored. Run `python data/fetch_data.py` to download them.

## Column Guide

Key columns from football-data.co.uk format:

| Column | Description |
|---|---|
| `Date` | Match date |
| `HomeTeam` / `AwayTeam` | Club names |
| `FTHG` / `FTAG` | Full-time goals (home/away) |
| `FTR` | Full-time result (H/D/A) |
| `HS` / `AS` | Shots (home/away) |
| `HST` / `AST` | Shots on target |
| `HC` / `AC` | Corners |
| `HY` / `AY` | Yellow cards |
| `HR` / `AR` | Red cards |
