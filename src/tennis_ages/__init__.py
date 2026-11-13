"""tennis_ages: plot a tennis player's age against their opponents' ages.

Public API
----------
get_player_career(player_name)
    Download a player's career matches from Tennis Abstract and return a
    clean data frame.
plot_player_career(career)
    Draw the age vs. age-difference scatter plot from that data frame.
"""

from tennis_ages.career import get_player_career
from tennis_ages.plot import plot_player_career

__all__ = ["get_player_career", "plot_player_career"]
