"""Public function that plots a player's career data frame."""

import matplotlib.pyplot as plt
import pandas as pd

REQUIRED_COLUMNS = ["player", "player_age", "age_difference", "result"]
COLORS = {"W": "#D99A00", "L": "#2F6FB0"}
LABELS = {"W": "Win", "L": "Loss"}


def _check_career(career: pd.DataFrame) -> None:
    """Raise a clear error unless `career` looks like get_player_career()'s output."""
    if not isinstance(career, pd.DataFrame) or career.empty:
        raise ValueError("career must be a non-empty data frame from get_player_career().")
    missing = [col for col in REQUIRED_COLUMNS if col not in career.columns]
    if missing:
        raise ValueError(f"career is missing columns: {', '.join(missing)}.")


def _draw_matches(ax: plt.Axes, career: pd.DataFrame) -> None:
    """Draw one point per match, colored by win or loss."""
    for result in ("W", "L"):
        matches = career[career["result"] == result]
        ax.scatter(
            matches["player_age"], matches["age_difference"], s=14, alpha=0.6,
            color=COLORS[result], edgecolors="none",
            label=f"{LABELS[result]} ({len(matches)})", zorder=2,
        )


def _style_axes(ax: plt.Axes, player_name: str) -> None:
    """Add the title, axis labels, legend and grid."""
    ax.set_title(f"{player_name}: age vs. age difference with opponents")
    ax.set_xlabel(f"{player_name}'s age (years)")
    ax.set_ylabel("Age difference: player minus opponent (years)")
    ax.legend(title="Result", frameon=False)
    ax.grid(alpha=0.3, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)


def plot_player_career(career: pd.DataFrame, ax: plt.Axes | None = None) -> plt.Axes:
    """Scatter plot of a player's age against their age difference with opponents.

    `career` is the data frame from get_player_career(). Each point is a
    match: x is the player's age, y is the player's age minus the opponent's
    (above the dashed line, the player was older), colored by win or loss.
    Pass `ax` to draw into an existing matplotlib Axes. Returns the Axes.
    """
    _check_career(career)
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8, zorder=1)
    _draw_matches(ax, career)
    _style_axes(ax, career["player"].iloc[0])
    return ax
