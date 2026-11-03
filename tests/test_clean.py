# tests for cleaning the career js files (no internet needed: uses mock files)
from pathlib import Path

import pytest

from tennis_career.clean import clean_career

DATA = Path(__file__).parent / "data"


@pytest.fixture
def female():
    text = (DATA / "FemalePlayerCareer.js").read_text()
    return clean_career(text, "Serena Williams", "19810926")


@pytest.fixture
def male():
    text = (DATA / "MalePlayerCareer.js").read_text()
    return clean_career(text, "Rafael Nadal", 19860603)


def test_one_row_per_match(female, male):
    assert len(female) == 3
    assert len(male) == 3


def test_columns(female):
    for col in ["player", "date", "opponent", "result",
                "player_age", "opp_age", "age_diff"]:
        assert col in female.columns


def test_player_name(female):
    assert (female["player"] == "Serena Williams").all()


def test_result_is_win_or_loss(female, male):
    assert list(female["result"]) == ["Loss", "Loss", "Loss"]
    assert list(male["result"]) == ["Loss", "Loss", "Win"]


def test_female_opponent_age_from_birthdate(female):
    # Anne Miller born 1977-01-19, match on 1995-10-30
    assert female.loc[0, "opponent"] == "Anne Miller"
    assert female.loc[0, "opp_age"] == pytest.approx(18.78)


def test_male_opponent_age_given(male):
    assert male.loc[0, "opponent"] == "Guillermo Platel"
    assert male.loc[0, "opp_age"] == pytest.approx(22.26)


def test_player_age(female, male):
    assert female.loc[0, "player_age"] == pytest.approx(14.09)
    assert male.loc[0, "player_age"] == pytest.approx(15.27)


def test_age_diff_is_player_minus_opponent(female, male):
    for career in [female, male]:
        diff = career["player_age"] - career["opp_age"]
        assert career["age_diff"].tolist() == pytest.approx(diff.tolist())


def test_missing_opponent_age_is_dropped():
    # one match where column 16 (opponent age) is empty
    row = ["20200101", "Tour", "Hard", "", "W", "", "", "", "R32", "6-0",
           "3", "Someone", "1", "", "", "R", "", "", "USA"]
    text = "var morematchmx = [" + str(row) + "];"
    assert len(clean_career(text, "Player", "20000101")) == 0


def test_bad_text_raises_error():
    with pytest.raises(ValueError):
        clean_career("not a js file", "P", "20000101")
