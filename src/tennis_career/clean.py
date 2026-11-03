# turn the text of a career js file into a clean data frame
import re
import ast
import pandas as pd

# positions of the columns I need in each match array
# (same for female and male files, only column 16 means something different)
COLUMNS = {
    0: "date",
    1: "tournament",
    2: "surface",
    4: "result",
    8: "round",
    9: "score",
    11: "opponent",
    16: "opp_dob_or_age",
    18: "opp_country",
}


def _parse_matches(js_text):
    """Turn the js array `var morematchmx = [[...], ...]` into a python list."""
    found = re.search(r"=\s*(\[.*\])", js_text, re.S)
    if found is None:
        raise ValueError("Could not find the match array in the js text.")
    return ast.literal_eval(found.group(1))


def _matches_to_frame(matches):
    """Keep only the columns in COLUMNS and give them names."""
    data = {name: [m[i] for m in matches] for i, name in COLUMNS.items()}
    return pd.DataFrame(data)


def _years_between(start, end):
    """Years from start to end (both datetime), rounded to 2 decimals."""
    return ((end - start).dt.days / 365.25).round(2)


def _has_birthdates(values):
    """Female files have opponent birthdates (YYYYMMDD), male files have ages."""
    return values.str.fullmatch(r"\d{8}").any()


def _opponent_age(career):
    """Opponent age at each match, from the birthdate or the age given."""
    values = career["opp_dob_or_age"]
    if _has_birthdates(values):
        opp_dob = pd.to_datetime(values, format="%Y%m%d", errors="coerce")
        return _years_between(opp_dob, career["date"])
    return pd.to_numeric(values, errors="coerce").round(2)


def clean_career(js_text, player_name, player_dob):
    """Clean the text of a career js file into a data frame for plotting.

    player_dob is the player's birthdate as "YYYYMMDD" (string or int).
    age_diff is positive when the player is older than the opponent.
    """
    career = _matches_to_frame(_parse_matches(js_text))
    career["date"] = pd.to_datetime(career["date"], format="%Y%m%d")
    career["result"] = career["result"].replace({"W": "Win", "L": "Loss"})
    dob = pd.to_datetime(str(player_dob), format="%Y%m%d")
    career["player_age"] = _years_between(dob, career["date"])
    career["opp_age"] = _opponent_age(career)
    career["age_diff"] = (career["player_age"] - career["opp_age"]).round(2)
    career.insert(0, "player", player_name)

    # drop matches where the opponent age is missing, then sort by date
    career = career.drop(columns="opp_dob_or_age").dropna(subset=["opp_age"])
    return career.sort_values("date").reset_index(drop=True)
