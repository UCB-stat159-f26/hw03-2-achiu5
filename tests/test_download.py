"""Tests for the private download helpers. The network is never used."""

import pytest

from tennis_ages import _download, get_player_career
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


def test_unknown_player_raises_meaningful_error(monkeypatch):
    requested = []

    def fake_fetch(url):
        requested.append(url)
        return None  # what _fetch_text returns when the page is a 404

    monkeypatch.setattr(_download, "_fetch_text", fake_fetch)
    with pytest.raises(ValueError, match="No Tennis Abstract career data found for 'GastonSanchez'"):
        get_player_career("GastonSanchez")
    assert requested == ["https://www.tennisabstract.com/jsmatches/GastonSanchezCareer.js"]
