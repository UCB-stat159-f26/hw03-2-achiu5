"""Tests for the private parsing helpers, run on the mock career JS files."""

import json

import pandas as pd
import pytest

from tennis_ages._parse import (
    _build_career_table,
    _extract_match_rows,
    _opponent_ages,
    _rows_to_frame,
)


def test_extract_match_rows_reads_female_file(female_js):
    rows = _extract_match_rows(female_js)
    assert len(rows) == 3
    assert rows[0][0] == "19951030"        # match date
    assert rows[0][11] == "Anne Miller"    # opponent
    assert rows[0][16] == "19770119"       # opponent's date of birth


def test_extract_match_rows_reads_male_file(male_js):
    rows = _extract_match_rows(male_js)
    assert len(rows) == 3
    assert rows[0][11] == "Guillermo Platel"
    assert rows[0][16] == "22.264202601"   # opponent's age, not a birth date


def test_opponent_ages_from_birth_dates(female_js):
    frame = _rows_to_frame(_extract_match_rows(female_js))
    match_dates = pd.to_datetime(frame["match_date"], format="%Y%m%d")
    ages = _opponent_ages(match_dates, frame["opponent_dob_or_age"])
    # e.g. Anne Miller, born 1977-01-19, was 18.78 on 1995-10-30
    assert ages.tolist() == pytest.approx([18.78, 26.84, 18.43], abs=0.01)


def test_opponent_ages_given_in_male_file(male_js):
    frame = _rows_to_frame(_extract_match_rows(male_js))
    match_dates = pd.to_datetime(frame["match_date"], format="%Y%m%d")
    ages = _opponent_ages(match_dates, frame["opponent_dob_or_age"])
    # Men's files already store the age, so it is used as-is.
    assert ages.tolist() == pytest.approx([22.264202601, 24.2902121834, 18.7597535934])


def test_build_career_table_columns_and_ages(female_js):
    career = _build_career_table(female_js, pd.Timestamp("1981-09-26"), "Serena Williams")
    assert list(career.columns) == [
        "player", "match_date", "tournament", "surface", "round", "opponent",
        "result", "score", "player_age", "opponent_age", "age_difference",
    ]
    assert len(career) == 3
    assert (career["player"] == "Serena Williams").all()
    assert career["match_date"].is_monotonic_increasing
    assert career["age_difference"].tolist() == pytest.approx(
        (career["player_age"] - career["opponent_age"]).tolist()
    )
    # First match: Serena was 14.09, Anne Miller 18.78, so -4.68
    first = career.iloc[0]
    assert first["player_age"] == pytest.approx(14.09, abs=0.01)
    assert first["age_difference"] == pytest.approx(-4.68, abs=0.01)


def test_build_career_table_drops_unplottable_matches(female_js):
    rows = _extract_match_rows(female_js)
    rows[1][4] = ""    # no W/L result (e.g. a walkover)
    rows[2][16] = ""   # no opponent date of birth
    js_text = "var morematchmx = " + json.dumps(rows)
    career = _build_career_table(js_text, pd.Timestamp("1981-09-26"), "Serena Williams")
    assert career["opponent"].tolist() == ["Anne Miller"]
