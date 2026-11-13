"""Smoke tests: the package installs and exposes exactly its public API."""

import tennis_ages


def test_public_api():
    assert tennis_ages.__all__ == ["get_player_career", "plot_player_career"]
    assert callable(tennis_ages.get_player_career)
    assert callable(tennis_ages.plot_player_career)
