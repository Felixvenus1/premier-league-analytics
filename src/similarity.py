"""Player similarity scoring using Euclidean or cosine distance."""

from __future__ import annotations

import numpy as np
import pandas as pd

DEFAULT_METRICS = [
    "goals_per90",
    "assists_per90",
    "shots_per90",
    "key_passes_per90",
    "dribbles_per90",
    "tackles_per90",
    "interceptions_per90",
    "aerials_won_per90",
]


def _normalise(matrix: np.ndarray) -> np.ndarray:
    """Min-max normalise each column to [0, 1]."""
    col_min = matrix.min(axis=0)
    col_max = matrix.max(axis=0)
    denom = col_max - col_min
    denom[denom == 0] = 1  # avoid divide-by-zero for constant columns
    return (matrix - col_min) / denom


def find_similar_players(
    df: pd.DataFrame,
    player_name: str,
    n: int = 5,
    metric: str = "euclidean",
    features: list[str] | None = None,
) -> pd.DataFrame:
    """Return the *n* most similar players to *player_name*.

    Parameters
    ----------
    df:
        DataFrame with a ``player`` column and numeric feature columns.
    player_name:
        Name to look up (case-sensitive).
    n:
        Number of similar players to return (excluding the target player).
    metric:
        ``"euclidean"`` or ``"cosine"``.
    features:
        Feature columns to use. Defaults to ``DEFAULT_METRICS`` (whichever
        are present in *df*).

    Returns
    -------
    DataFrame with columns ``player``, ``distance``, sorted ascending.
    """
    if player_name not in df["player"].values:
        raise ValueError(f"Player not found: {player_name!r}")

    cols = [c for c in (features or DEFAULT_METRICS) if c in df.columns]
    if not cols:
        raise ValueError("No valid feature columns found in dataframe.")

    sub = df[["player"] + cols].dropna(subset=cols).reset_index(drop=True)
    matrix = _normalise(sub[cols].to_numpy(dtype=float))

    idx = sub.index[sub["player"] == player_name][0]
    target = matrix[idx]

    if metric == "euclidean":
        dists = np.linalg.norm(matrix - target, axis=1)
    elif metric == "cosine":
        norms = np.linalg.norm(matrix, axis=1) * np.linalg.norm(target)
        norms[norms == 0] = 1
        dists = 1 - (matrix @ target) / norms
    else:
        raise ValueError(f"Unknown metric: {metric!r}. Use 'euclidean' or 'cosine'.")

    order = np.argsort(dists)
    order = order[order != idx][:n]

    result = sub.loc[order, ["player"]].copy()
    result["distance"] = dists[order]
    return result.reset_index(drop=True)
