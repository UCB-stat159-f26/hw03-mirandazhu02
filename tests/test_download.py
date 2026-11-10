# tests for helpers in download.py: player names and js variables
# (no internet needed: these do not download anything)
from tennis_career.download import _js_value, _name_param


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


def test_js_value_reads_numbers_and_text():
    # same style as the top of a player's js file, e.g. JuanMartinDelPotro.js
    js_text = ("var fullname = 'Juan Martin Del Potro';\n"
               "var lastname = 'Del Potro';\nvar dob=19880923;\n")
    assert _js_value(js_text, "fullname") == "Juan Martin Del Potro"
    assert _js_value(js_text, "lastname") == "Del Potro"
    assert _js_value(js_text, "dob") == "19880923"


def test_js_value_missing():
    assert _js_value("var dob=19880923;", "lastname") is None
