# scatter plot of a player's matches like the NYT graphic (HW2)
import math

import matplotlib.pyplot as plt

WIN_COLOR = "#5bb8e3"
LOSS_COLOR = "#7b2a8c"
GRAY = "gray"


def _draw_points(ax, career, last_name):
    """One dot per match: blue for wins, purple for losses."""
    for result, color, label in [("Win", WIN_COLOR, f"Match {last_name} won"),
                                 ("Loss", LOSS_COLOR, "Match lost")]:
        rows = career[career["result"] == result]
        ax.scatter(rows["player_age"], rows["age_diff"], s=22, color=color,
                   alpha=0.85, linewidths=0, label=label, zorder=3)


def _style_age_axis(ax, ages, last_name):
    """Player's age on the top axis, one tick every 2 years."""
    first, last = 2 * math.floor(ages.min() / 2), 2 * math.floor(ages.max() / 2)
    ax.set_xticks(range(first, last + 1, 2))
    ax.xaxis.tick_top()
    ax.annotate(f"{last_name}'s age:", xy=(0, 1), xytext=(-20, 4),
                xycoords="axes fraction", textcoords="offset points",
                ha="right", va="bottom", color=GRAY, fontsize=11)


def _diff_labels(ticks):
    """'-10', 'Same age', '+10', '+20 years' (only the top one says years)."""
    labels = ["Same age" if t == 0 else f"{t:+d}" for t in ticks]
    labels[-1] += " years"
    return labels


def _style_diff_axis(ax, diffs):
    """Age difference on the y axis, symmetric, one tick every 10 years."""
    biggest = diffs.abs().max()
    limit = 10 * max(1, round(biggest / 10))
    ticks = list(range(-limit, limit + 1, 10))
    ax.set_yticks(ticks, _diff_labels(ticks))
    ax.set_ylim(-max(limit, biggest) - 1, max(limit, biggest) + 1)
    ax.axhline(0, color="dimgray", linewidth=1.2, zorder=2)
    _add_side_labels(ax, limit)


def _add_side_labels(ax, limit):
    """'Older than opponent' above and 'Younger than opponent' below 0."""
    side = ax.get_yaxis_transform()
    for y, text in [(0.75 * limit, "Older than\nopponent"),
                    (-0.75 * limit, "Younger than\nopponent")]:
        ax.text(-0.025, y, text, transform=side, ha="right", va="center",
                color=GRAY, fontsize=11)


def _style_frame(ax):
    """Light grid, no box around the plot, gray tick labels."""
    ax.grid(color="#dddddd", linewidth=0.8, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0, colors=GRAY, labelsize=11)


def plot_career(career):
    """Scatter plot of a player's age vs. how much older than each opponent.

    career is the data frame returned by get_career_data().
    Returns the matplotlib Axes so the plot can be changed or saved.
    """
    name = career["player"].iloc[0]
    last_name = name.split()[-1]
    ages = career["player_age"]
    fig, ax = plt.subplots(figsize=(10, 6.5))
    _draw_points(ax, career, last_name)
    _style_age_axis(ax, ages, last_name)
    _style_diff_axis(ax, career["age_diff"])
    _style_frame(ax)
    fig.suptitle(f"{name}'s Professional Matches, Age "
                 f"{math.floor(ages.min())} to {math.floor(ages.max())}",
                 fontsize=16, fontweight="bold")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.07), ncol=2,
              frameon=False, fontsize=11)
    fig.text(0.5, 0.01, "Source: Tennis Abstract", ha="center", color=GRAY)
    fig.tight_layout()
    return ax
