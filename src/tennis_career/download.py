# download a player's career js file and birthdate from tennis abstract
import re

import requests

from tennis_career.clean import clean_career

BASE_URL = "https://www.tennisabstract.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _capitalize(word):
    """'serena' -> 'Serena', but keep 'McEnroe' as it is."""
    if word.islower() or word.isupper():
        return word.capitalize()
    return word[0].upper() + word[1:]


def _name_param(player_name):
    """'serena williams' or 'Serena Williams' -> 'SerenaWilliams'."""
    words = re.split(r"[^A-Za-z]+", player_name)
    return "".join(_capitalize(w) for w in words if w)


def _fetch(url):
    """Text of a web page, or None if the page does not exist (404)."""
    response = requests.get(url, headers=HEADERS, timeout=30)
    if response.status_code == 404:
        return None
    if response.status_code == 429:
        raise RuntimeError("Tennis Abstract got too many requests. "
                           "Please wait a minute and try again.")
    response.raise_for_status()
    return response.text


def _download_career_js(name_param):
    """Text of the player's career js file, e.g. SerenaWilliamsCareer.js."""
    js_text = _fetch(f"{BASE_URL}/jsmatches/{name_param}Career.js")
    if js_text is None:
        raise ValueError(
            f"Could not find a player called '{name_param}' on Tennis Abstract."
            " Check the spelling, e.g. 'Serena Williams' or 'Rafael Nadal'."
        )
    return js_text


def _download_player_info(name_param):
    """Full name and birthdate (YYYYMMDD) from the player's js file."""
    page = _fetch(f"{BASE_URL}/jsmatches/{name_param}.js") or ""
    dob = re.search(r"dob\s*=\s*(\d{8})", page)
    fullname = re.search(r"fullname\s*=\s*'([^']+)'", page)
    if dob is None:
        raise ValueError(f"Could not find the birthdate of '{name_param}'.")
    return (fullname.group(1) if fullname else name_param), dob.group(1)


def get_career_data(player_name):
    """Get a clean data frame of a player's career matches.

    player_name can be written like "serena williams", "Serena Williams"
    or "SerenaWilliams". Raises ValueError if the player is not found.
    """
    name_param = _name_param(player_name)
    if not name_param:
        raise ValueError("Please give the name of a player, e.g. 'Serena Williams'.")
    js_text = _download_career_js(name_param)
    fullname, dob = _download_player_info(name_param)
    return clean_career(js_text, fullname, dob)
