"""Tests for the private parsing helpers, run on the mock career JS files."""

import pandas as pd
import pytest

from tennis_ages._parse import _extract_match_rows, _opponent_ages, _rows_to_frame


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
