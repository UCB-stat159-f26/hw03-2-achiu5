"""Private helpers that turn a player name into URLs and download their text.

Nothing in this module is tested against the live site; tests cover only the
pure helpers, such as name normalization.
"""

import re
import urllib.error
import urllib.request

import pandas as pd

BASE_URL = "https://www.tennisabstract.com"
USER_AGENT = "Mozilla/5.0 (compatible; tennis_ages Python package)"


def _to_url_name(player_name: str) -> str:
    """Turn "serena williams" / "Serena Williams" / "SerenaWilliams" into
    "SerenaWilliams", the form Tennis Abstract uses in its URLs."""
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError(
            "player_name must be a non-empty string, e.g. 'Serena Williams'."
        )
    # Capitalize only the first letter of each word so internal capitals,
    # as in "SerenaWilliams", are kept.
    return "".join(word[:1].upper() + word[1:] for word in player_name.split())


def _handle_http_error(error: urllib.error.HTTPError) -> None:
    """Return None for a missing page (404); otherwise raise a clear error."""
    if error.code == 404:
        return None
    if error.code == 429:
        raise ConnectionError(
            "Tennis Abstract is limiting requests right now. Wait a minute "
            "and try again."
        ) from error
    raise error


def _fetch_text(url: str) -> str | None:
    """Download `url` and return its text, or None if the page doesn't exist."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        return _handle_http_error(error)


def _download_career_js(url_name: str) -> str:
    """Download the player's career JS file; a missing file means a bad name."""
    js_text = _fetch_text(f"{BASE_URL}/jsmatches/{url_name}Career.js")
    if js_text is None:
        raise ValueError(
            f"No Tennis Abstract career data found for '{url_name}'. Check the "
            "spelling of the player's full name, e.g. 'Serena Williams'."
        )
    return js_text


def _download_player_info(url_name: str) -> tuple[str, pd.Timestamp]:
    """Return the player's full name and date of birth from their player page.

    The career JS file doesn't contain the player's own date of birth, but the
    player page defines it as `var dob = YYYYMMDD;` (for women and men alike).
    """
    page = _fetch_text(f"{BASE_URL}/cgi-bin/player.cgi?p={url_name}") or ""
    dob = re.search(r"var dob = (\d{8});", page)
    if dob is None:
        raise ValueError(f"Tennis Abstract has no date of birth for '{url_name}'.")
    full_name = re.search(r"var fullname = '([^']+)';", page)
    name = full_name.group(1) if full_name else url_name
    return name, pd.to_datetime(dob.group(1), format="%Y%m%d")
