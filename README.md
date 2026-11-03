# tennis_career

A Python package to get a tennis player's career matches from
[Tennis Abstract](https://www.tennisabstract.com) and plot them like the
NYT graphic about Serena Williams (HW2).

## Installation

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-mirandazhu02.git
```

## Usage

```python
from tennis_career import get_career_data, plot_career

# Serena Williams data and plot
serena = get_career_data("serena williams")
plot_career(serena)

# Rafael Nadal data and plot
rafa = get_career_data("Rafael Nadal")
plot_career(rafa)

# raises a ValueError with a message saying the player was not found
unknown_player = get_career_data("GastonSanchez")
```

`get_career_data()` accepts names like `"serena williams"`,
`"Serena Williams"` or `"SerenaWilliams"`. `plot_career()` returns the
matplotlib Axes, so in a script you may need `plt.show()` or
`plt.savefig("plot.png")` to see the plot.

## The data frame

Each row is one match. The main columns are:

| column | meaning |
|---|---|
| `player` | full name of the player |
| `date` | start date of the tournament |
| `opponent` | name of the opponent |
| `result` | `Win` or `Loss` (from the player's point of view) |
| `player_age` | player's age on the match date (years) |
| `opp_age` | opponent's age on the match date (years) |
| `age_diff` | `player_age - opp_age`, positive when the player is older |

It also has `tournament`, `surface`, `round`, `score` and `opp_country`.

## How it works

- The matches come from `jsmatches/<Name>Career.js`. The player's
  birthdate comes from `jsmatches/<Name>.js`.
- Career files of female players have the opponent's birthdate, so the
  opponent's age is calculated as (match date - birthdate) / 365.25.
  Career files of male players already have the opponent's age.
- Matches where the opponent's age is missing are dropped.
- The date is the start date of the tournament, so ages can be off by a
  week or two.
- The data only covers what Tennis Abstract has in the career file. For
  some players (for example Rafael Nadal), recent seasons are not in it.

## Tests

The tests do not use the internet. They use the mock files
`tests/data/FemalePlayerCareer.js` and `tests/data/MalePlayerCareer.js`.

```bash
pip install -e ".[test]"
pytest
```

## Reflections

<!-- TODO (Miranda): write what you learned while working on this assignment -->
