# tennis-ages

A Python package that downloads a tennis player's career singles matches from
[Tennis Abstract](https://www.tennisabstract.com) and plots the player's age
against how much older or younger each opponent was, like the *New York Times*
Serena Williams graphic from HW2 (without its annotations).

Stat 159, Homework 3.

## Installation

Install directly from GitHub with `pip`:

```bash
# Python package
pip install git+https://github.com/username/yourpackage.git
```

For this repository, that is:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-2-achiu5.git
```

This installs the `tennis_ages` package and its dependencies, `pandas` and
`matplotlib`. It requires Python 3.10 or newer.

## Usage

```python
import matplotlib.pyplot as plt
from tennis_ages import get_player_career, plot_player_career

# Serena Williams data and plot
serena = get_player_career("serena williams")
plot_player_career(serena)

# Rafael Nadal data and plot
rafa = get_player_career("Rafael Nadal")
plot_player_career(rafa)

plt.show()  # only needed in a script; notebooks show plots automatically

# raises a ValueError with a meaningful message
unknown_player = get_player_career("GastonSanchez")
```

## Public functions

The package has two public functions, both importable from `tennis_ages`.

### `get_player_career(player_name)`

Downloads a player's career singles matches from Tennis Abstract and returns
a clean data frame with one row per match, sorted by date.

- **`player_name`**: the player's name, written like `"serena williams"`,
  `"Serena Williams"` or `"SerenaWilliams"`.
- **Returns** a `pandas.DataFrame` with these columns:

  | Column | Description |
  |---|---|
  | `player` | The player's full name, e.g. `"Serena Williams"` |
  | `match_date` | Date of the match |
  | `tournament` | Tournament name |
  | `surface` | Court surface (Hard, Clay, Grass, Carpet) |
  | `round` | Round, e.g. `Q1`, `R32`, `F` |
  | `opponent` | Opponent's name |
  | `result` | `"W"` (win) or `"L"` (loss) |
  | `score` | Match score |
  | `player_age` | The player's age on the match date, in years |
  | `opponent_age` | The opponent's age on the match date, in years |
  | `age_difference` | `player_age` minus `opponent_age`; positive means the player was older |

- **Raises**
  - `ValueError` if Tennis Abstract has no career data for the name, e.g.
    *"No Tennis Abstract career data found for 'GastonSanchez'. Check the
    spelling of the player's full name, e.g. 'Serena Williams'."*
  - `ValueError` if `player_name` is empty or not a string.
  - `ConnectionError` if Tennis Abstract is limiting requests (HTTP 429);
    wait a minute and try again.

### `plot_player_career(career, ax=None)`

Draws a scatter plot from the data frame returned by `get_player_career()`.

- **x-axis**: the player's age.
- **y-axis**: the player's age minus the opponent's age. A dashed line at 0
  marks matches against someone the same age; above it, the player was older.
- **Colors**: wins in gold, losses in blue, with the number of each in the
  legend.
- **`ax`** (optional): a matplotlib `Axes` to draw into, e.g. to put two
  players side by side. If omitted, a new figure is created.
- **Returns** the matplotlib `Axes`, so the plot can be customized or saved,
  e.g. `plot_player_career(serena).figure.savefig("serena.png")`.
- **Raises** `ValueError` if `career` is not a non-empty data frame or is
  missing any of the columns `player`, `player_age`, `age_difference` or
  `result`.

## How the data is built

1. **Player name to URL.** The name is turned into Tennis Abstract's URL form,
   e.g. `"serena williams"` becomes `SerenaWilliams`.
2. **Match data.** The career file
   `https://www.tennisabstract.com/jsmatches/<Name>Career.js` is downloaded.
   It holds one JavaScript array, `var morematchmx = [[...], ...]`, with one
   row per match and no header. If the file doesn't exist (404), the name is
   reported as invalid.
3. **Player's date of birth.** The career file doesn't contain the player's
   own date of birth, so it is read from the player page
   (`cgi-bin/player.cgi?p=<Name>`), which defines `var dob = YYYYMMDD;`.
4. **Parsing.** Rows have different lengths (recent matches carry extra
   statistics), so columns are picked by position.
5. **Ages.** Column 16 differs between women's and men's files:
   - women's files store the **opponent's date of birth** (e.g. `19770119`),
     from which the opponent's age on the match date is calculated;
   - men's files already store the **opponent's age** (e.g. `22.264202601`).

   The package detects which format a file uses from the values themselves.
   Ages are measured in years of 365.25 days.
6. **Cleaning.** Matches with no W/L result or no usable age are dropped,
   since they can't be plotted.

### Limitations

- An internet connection is needed to download the data.
- Matches come only from the `Career.js` file, and some of those files are not
  fully up to date. For example, Rafael Nadal's file stops in October 2016,
  so his plot ends at age 30 even though he played until 2024.

## Package layout

Every function is at most 20 lines of code (excluding comments and blank
lines), and the private helpers are at most 10.

```
pyproject.toml              package metadata, dependencies, pytest settings
LICENSE                     MIT license
src/tennis_ages/
    __init__.py             exports the two public functions
    career.py               get_player_career()
    plot.py                 plot_player_career()
                            + private: _check_career, _draw_matches, _style_axes
    _download.py            private: player name -> URL -> downloaded text
                                _to_url_name, _fetch_text, _handle_http_error,
                                _download_career_js, _download_player_info
    _parse.py               private: career JS text -> clean data frame
                                _extract_match_rows, _rows_to_frame,
                                _parse_dates, _years_between, _opponent_ages,
                                _add_ages, _build_career_table
tests/
    conftest.py             fixtures that read the mock JS files
    fixtures/
        FemalePlayerCareer.js   mock women's career file (from the assignment)
        MalePlayerCareer.js     mock men's career file (from the assignment)
    test_package.py
    test_parse.py
    test_download.py
    test_plot.py
```

Modules and functions whose names start with `_` are private helpers and are
not part of the public API.

## Tests

The tests never contact tennisabstract.com. The parsing code runs on the mock
career files in `tests/fixtures/`, and the download code runs with the network
replaced by a fake (pytest's `monkeypatch`).

To run them from a clone of this repository:

```bash
pip install -e ".[test]"
pytest -v
```

| File | What it tests |
|---|---|
| `test_package.py` | The package exports exactly the two public functions. |
| `test_parse.py` | Reading the match rows from the women's and men's mock files; calculating opponent ages from dates of birth (women) vs. using the given ages (men); the clean data frame's columns, sort order and `age_difference`, checked against known values (Serena was 14.09 and 4.68 years younger than Anne Miller at her first match); dropping matches with no result or no age. |
| `test_download.py` | All three name formats give the same URL name; empty or non-string names are rejected; an unknown player (`"GastonSanchez"`) raises a meaningful `ValueError` after one request; the player's full name and date of birth are read from the player page. |
| `test_plot.py` | The plot has one set of points for wins and one for losses, drawn at x = `player_age` and y = `age_difference`, with the player's name in the title; empty, non-data-frame and incomplete input raise `ValueError`. |

## Reflections

The key takeaways from this assignment include how to create a Python package out of your analysis. It was helpful to break the code into functions which download, clean, and plot the data separately. One thing I had to take into account was the fact that the formats of data are slightly different – the files for women include the birth dates of their opponents, while those for men include only the opponents' age. Making both the data in one format allowed me to use the same function to plot both kinds of data. Testing the package locally with mock files and mock downloads was helpful because it helped me to test my parsing and data cleaning without having to use the site itself. The drawback is that the package requires Tennis Abstract to have the data in that exact structure and leaves the matches out if they do not have all the required information.
