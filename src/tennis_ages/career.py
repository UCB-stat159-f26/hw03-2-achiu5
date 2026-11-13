"""Public function that returns a player's clean career data frame."""

import pandas as pd

from tennis_ages._download import (
    _download_career_js,
    _download_player_info,
    _to_url_name,
)
from tennis_ages._parse import _build_career_table


def get_player_career(player_name: str) -> pd.DataFrame:
    """Download a player's career singles matches from Tennis Abstract."""
    url_name = _to_url_name(player_name)
    js_text = _download_career_js(url_name)
    full_name, player_dob = _download_player_info(url_name)
    return _build_career_table(js_text, player_dob, full_name)
