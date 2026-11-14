"""Tests for the private parsing helpers, run on the mock career JS files."""

from tennis_ages._parse import _extract_match_rows


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
