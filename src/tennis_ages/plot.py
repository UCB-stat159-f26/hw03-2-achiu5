"""Public function that plots a player's career data frame."""

import pandas as pd


def plot_player_career(career: pd.DataFrame):
    """Scatter plot of the player's age against the age difference.

    Parameters
    ----------
    career : pandas.DataFrame
        The data frame returned by `get_player_career()`.

    Returns
    -------
    matplotlib.axes.Axes
        The axes holding the plot. The x-axis is the player's age, the y-axis
        is the player's age minus the opponent's age, and points are colored
        by win or loss.
    """
    raise NotImplementedError
