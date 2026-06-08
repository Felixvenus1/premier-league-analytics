"""Tests for src/similarity.py."""

import numpy as np
import pandas as pd
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.similarity import find_similar_players, _normalise


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "player": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
            "goals_per90": [0.8, 0.1, 0.75, 0.2, 0.05],
            "assists_per90": [0.3, 0.6, 0.35, 0.55, 0.7],
            "shots_per90": [3.0, 1.0, 2.8, 1.2, 0.9],
            "key_passes_per90": [1.0, 2.5, 1.1, 2.3, 2.8],
        }
    )


def test_returns_n_results(sample_df):
    result = find_similar_players(sample_df, "Alice", n=2)
    assert len(result) == 2


def test_does_not_include_target(sample_df):
    result = find_similar_players(sample_df, "Alice", n=4)
    assert "Alice" not in result["player"].values


def test_euclidean_closest_player(sample_df):
    result = find_similar_players(sample_df, "Alice", n=1, metric="euclidean")
    # Charlie has the most similar profile to Alice (both high goals, high shots)
    assert result.iloc[0]["player"] == "Charlie"


def test_cosine_returns_valid_distances(sample_df):
    result = find_similar_players(sample_df, "Bob", n=3, metric="cosine")
    assert (result["distance"] >= 0).all()
    assert (result["distance"] <= 2).all()  # cosine distance is in [0, 2]


def test_sorted_ascending(sample_df):
    result = find_similar_players(sample_df, "Alice", n=4)
    dists = result["distance"].tolist()
    assert dists == sorted(dists)


def test_unknown_player_raises(sample_df):
    with pytest.raises(ValueError, match="Player not found"):
        find_similar_players(sample_df, "Zara", n=2)


def test_unknown_metric_raises(sample_df):
    with pytest.raises(ValueError, match="Unknown metric"):
        find_similar_players(sample_df, "Alice", n=2, metric="manhattan")


def test_custom_features(sample_df):
    result = find_similar_players(
        sample_df, "Alice", n=2, features=["goals_per90", "shots_per90"]
    )
    assert len(result) == 2


def test_normalise_range():
    matrix = np.array([[0.0, 10.0], [5.0, 20.0], [10.0, 30.0]])
    out = _normalise(matrix)
    assert out.min() == pytest.approx(0.0)
    assert out.max() == pytest.approx(1.0)


def test_normalise_constant_column():
    matrix = np.array([[5.0, 1.0], [5.0, 2.0], [5.0, 3.0]])
    out = _normalise(matrix)
    # constant column → all zeros, should not raise
    assert (out[:, 0] == 0).all()
