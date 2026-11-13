# tennis-ages

A Python package that downloads a tennis player's career singles matches from
[Tennis Abstract](https://www.tennisabstract.com) and plots the player's age
against how much older or younger each opponent was, like the *New York Times*
Serena Williams graphic (without its annotations).

Stat 159, Homework 3.

## Installation

```bash
pip install git+https://github.com/<username>/<repo>.git
```

## Usage

```python
from tennis_ages import get_player_career, plot_player_career

serena = get_player_career("serena williams")
plot_player_career(serena)

rafa = get_player_career("Rafael Nadal")
plot_player_career(rafa)

get_player_career("GastonSanchez")  # raises a clear error
```

## Package layout

```
pyproject.toml          package metadata and dependencies
src/tennis_ages/
    __init__.py         exports the two public functions
    career.py           get_player_career()
    plot.py             plot_player_career()
    _download.py        private: player name -> URL -> file text
    _parse.py           private: JS text -> clean data frame
tests/
    conftest.py         shared fixtures
    fixtures/           mock men's and women's career JS files
    test_*.py           tests (no network access)
```

## Running the tests

```bash
pip install -e ".[test]"
pytest
```

The tests never contact tennisabstract.com. They run the parsing and cleaning
code against the mock files in `tests/fixtures/`.

## Reflections

*To be written.*
