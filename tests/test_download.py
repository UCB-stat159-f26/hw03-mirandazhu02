# tests for turning a player name into the name used in tennis abstract urls
# (no internet needed: these do not download anything)
from tennis_career.download import _name_param


def test_name_with_space():
    assert _name_param("serena williams") == "SerenaWilliams"
    assert _name_param("Rafael Nadal") == "RafaelNadal"


def test_name_already_joined():
    assert _name_param("SerenaWilliams") == "SerenaWilliams"


def test_name_with_hyphen_and_extra_spaces():
    assert _name_param("  jo-wilfried   tsonga ") == "JoWilfriedTsonga"


def test_name_in_capitals():
    assert _name_param("SERENA WILLIAMS") == "SerenaWilliams"


def test_empty_name():
    assert _name_param("   ") == ""
