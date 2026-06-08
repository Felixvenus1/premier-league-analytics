"""Reusable chart helpers for Premier League analysis."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def radar_chart(
    df: pd.DataFrame,
    players: list[str],
    features: list[str],
    ax: plt.Axes | None = None,
    title: str = "Player Radar",
) -> plt.Axes:
    """Draw a radar / spider chart for *players* across *features*."""
    n = len(features)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    if ax is None:
        _, ax = plt.subplots(subplot_kw={"polar": True}, figsize=(6, 6))

    sub = df.set_index("player")[features]
    # min-max normalise within the selected rows for visual comparability
    norm = (sub - sub.min()) / (sub.max() - sub.min()).replace(0, 1)

    for player in players:
        if player not in norm.index:
            continue
        values = norm.loc[player].tolist() + norm.loc[player].tolist()[:1]
        ax.plot(angles, values, label=player)
        ax.fill(angles, values, alpha=0.1)

    ax.set_thetagrids(np.degrees(angles[:-1]), features)
    ax.set_title(title, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    return ax


def ranked_bar(
    series: pd.Series,
    title: str = "",
    xlabel: str = "",
    top_n: int = 20,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Horizontal ranked bar chart for the top-*n* entries in *series*."""
    data = series.nlargest(top_n).iloc[::-1]
    if ax is None:
        _, ax = plt.subplots(figsize=(8, top_n * 0.35 + 1))
    ax.barh(data.index, data.values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    return ax
