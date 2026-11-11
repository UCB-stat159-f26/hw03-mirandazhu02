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
| `last_name` | last name of the player (used in the plot labels) |
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
- Some current players (for example Carlos Alcaraz and Jannik Sinner) have
  a page on Tennis Abstract but no career file. For them,
  `get_career_data()` raises an error that says so, instead of saying the
  player does not exist.

## Tests

The tests do not use the internet. They use the mock files
`tests/data/FemalePlayerCareer.js` and `tests/data/MalePlayerCareer.js`.

```bash
pip install -e ".[test]"
pytest
```

## Reflections

The biggest thing I learned from this assignment is how different a
script for myself is from a tool for other people. My HW2 cleaning
script only worked for Serena Williams because three things were
hard-coded: the file path, her birthdate (26-Sep-1981), and the
assumption that column 16 is the opponent's birthdate. As soon as I
tried Rafael Nadal, column 16 held an age like "22.264202601" instead of
a date like "19770119", and the player's own birthdate was not in the
Career.js file at all, so it had to come from another file. Turning the
script into a package meant finding every one of these assumptions and
making it work for any player.

I also learned that the data source has limits that no code can fix.
Nadal played until 2024, but his Career.js file stops in 2016, when he
was 30. Carlos Alcaraz and Jannik Sinner have pages on Tennis Abstract
but no career file, so at first the package wrongly said they did not
exist. For Sinner there was an old file with only 34 matches from 2018,
and I decided not to use it, because plotting it as his "career" would
be misleading. Instead the error message now says the player exists but
has no career file, and the README explains this limit.

Writing tests changed how I think about checking my work. Because the
tests use the mock files instead of the website, I can check exact
values, like Anne Miller being 18.78 years old at the 1995 Canadian
Open, and they still pass with the internet turned off. This mattered
because Tennis Abstract blocked us with "Too Many Requests" while we
were testing. The 20-line limit also forced me to split the code into
small functions such as `_has_birthdates()`, which made each step easier
to understand and test. One bug I would not have found otherwise was
that the tests failed in a fresh clone because pytest could not find the
package.

I used Claude Code a lot in this assignment, and it wrote most of the
first version of the code. My part was checking the requirements, running
everything in my own terminal, and deciding what to keep. Even running
it taught me something: `pip` and `python` in my terminal pointed to two
different Pythons, so the package was installed but could not be
imported until I used `python -m pip`. I also learned that the commit
history should show how the work really happened. At first I worried
that most commits were on the same day, but I kept the real dates and
made the later fixes as new commits instead.
