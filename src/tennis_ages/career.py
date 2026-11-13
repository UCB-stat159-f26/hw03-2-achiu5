"""Public function that returns a player's clean career data frame."""

import pandas as pd


def get_player_career(player_name: str) -> pd.DataFrame:
    """Return one row per career singles match for `player_name`.

    Parameters
    ----------
    player_name : str
        The player's name, e.g. "serena williams", "Serena Williams" or
        "SerenaWilliams".

    Returns
    -------
    pandas.DataFrame
        One row per match, with the player's age, the opponent's age, their
        difference, and the match result (W or L).

    Raises
    ------
    ValueError
        If Tennis Abstract has no career file for `player_name`.
    """
    raise NotImplementedError
