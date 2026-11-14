"""Tests for the private download helpers. The network is never used."""

import pytest

from tennis_ages._download import _to_url_name


@pytest.mark.parametrize(
    "player_name",
    ["serena williams", "Serena Williams", "SerenaWilliams", "  serena   williams "],
)
def test_to_url_name_accepts_all_formats(player_name):
    assert _to_url_name(player_name) == "SerenaWilliams"


@pytest.mark.parametrize("player_name", ["", "   ", None, 42])
def test_to_url_name_rejects_empty_or_non_text(player_name):
    with pytest.raises(ValueError, match="non-empty string"):
        _to_url_name(player_name)
