"""Private helpers that parse and clean a Tennis Abstract career JS file.

These work on the file's text, not on the network, so they are what the test
suite covers using the mock files in tests/fixtures/.

The file holds one JavaScript array, `var morematchmx = [[...], ...]`, with no
header row. Rows have different lengths (recent matches carry extra stats), so
columns are picked by position. Women's files store the opponent's date of
birth (YYYYMMDD) in column 16; men's files store the opponent's age in years.
"""

import json
import re

import pandas as pd

MATCH_TABLE = re.compile(r"var\s+morematchmx\s*=\s*(\[.*\])", re.S)

# Position in each raw row -> column name.
RAW_COLUMNS = {
    0: "match_date",
    1: "tournament",
    2: "surface",
    4: "result",
    8: "round",
    9: "score",
    11: "opponent",
    16: "opponent_dob_or_age",
}

OUTPUT_COLUMNS = [
    "player", "match_date", "tournament", "surface", "round", "opponent",
    "result", "score", "player_age", "opponent_age", "age_difference",
]


def _extract_match_rows(js_text: str) -> list[list[str]]:
    """Return the rows of the `morematchmx` array in a career JS file."""
    match = MATCH_TABLE.search(js_text)
    if match is None:
        raise ValueError("Could not find the 'morematchmx' table in the file.")
    return json.loads(match.group(1))


def _rows_to_frame(rows: list[list[str]]) -> pd.DataFrame:
    """Keep only the columns in RAW_COLUMNS, picked by position."""
    width = max(RAW_COLUMNS) + 1
    records = [[row[i] for i in RAW_COLUMNS] for row in rows if len(row) >= width]
    return pd.DataFrame(records, columns=list(RAW_COLUMNS.values()))


def _parse_dates(yyyymmdd: pd.Series) -> pd.Series:
    """Parse YYYYMMDD strings into dates; unparseable values become NaT."""
    return pd.to_datetime(yyyymmdd, format="%Y%m%d", errors="coerce")


def _years_between(start_dates, end_dates) -> pd.Series:
    """Years from start to end, using 365.25-day years."""
    return (end_dates - start_dates) / pd.Timedelta(days=365.25)


def _opponent_ages(match_dates: pd.Series, dob_or_age: pd.Series) -> pd.Series:
    """Opponent ages, from birth dates (women's files) or given ages (men's)."""
    # An 8-digit value is a YYYYMMDD birth date; ages have a decimal point.
    if dob_or_age.str.fullmatch(r"\d{8}").any():
        return _years_between(_parse_dates(dob_or_age), match_dates)
    return pd.to_numeric(dob_or_age, errors="coerce")


def _add_ages(career: pd.DataFrame, player_dob: pd.Timestamp) -> pd.DataFrame:
    """Add the player_age, opponent_age and age_difference columns."""
    dates = career["match_date"]
    career["opponent_age"] = _opponent_ages(dates, career["opponent_dob_or_age"])
    career["player_age"] = _years_between(player_dob, dates)
    career["age_difference"] = career["player_age"] - career["opponent_age"]
    return career


def _build_career_table(
    js_text: str, player_dob: pd.Timestamp, player_name: str
) -> pd.DataFrame:
    """Turn a career JS file into the clean, one-row-per-match data frame."""
    career = _rows_to_frame(_extract_match_rows(js_text))
    career["match_date"] = _parse_dates(career["match_date"])
    career = _add_ages(career, player_dob).assign(player=player_name)
    # Drop matches with no W/L result or no age, since they can't be plotted.
    career = career[career["result"].isin(["W", "L"])]
    career = career.dropna(subset=["match_date", "player_age", "opponent_age"])
    return career[OUTPUT_COLUMNS].sort_values("match_date", ignore_index=True)
