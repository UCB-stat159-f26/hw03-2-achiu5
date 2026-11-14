"""Tests for plot_player_career, using a data frame built from a mock JS file."""

import matplotlib

matplotlib.use("Agg")  # draw off-screen so no windows open during tests
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402

from tennis_ages import plot_player_career  # noqa: E402
from tennis_ages._parse import _build_career_table  # noqa: E402


@pytest.fixture
def male_career(male_js):
    """Clean data frame for the men's mock file (Nadal's first 3 matches)."""
    return _build_career_table(male_js, pd.Timestamp("1986-06-03"), "Rafael Nadal")


def test_plot_player_career_draws_wins_and_losses(male_career):
    ax = plot_player_career(male_career)
    wins, losses = ax.collections          # one set of points per result
    assert len(wins.get_offsets()) == 1     # 1 win in the mock file
    assert len(losses.get_offsets()) == 2   # 2 losses
    win = male_career[male_career["result"] == "W"].iloc[0]
    assert tuple(wins.get_offsets()[0]) == pytest.approx(
        (win["player_age"], win["age_difference"])
    )
    assert ax.get_title() == "Rafael Nadal: age vs. age difference with opponents"
    plt.close(ax.figure)


def test_plot_player_career_rejects_bad_input(male_career):
    with pytest.raises(ValueError, match="non-empty data frame"):
        plot_player_career(pd.DataFrame())                 # empty
    with pytest.raises(ValueError, match="non-empty data frame"):
        plot_player_career("serena williams")              # a name, not data
    with pytest.raises(ValueError, match="missing columns: result"):
        plot_player_career(male_career.drop(columns="result"))
