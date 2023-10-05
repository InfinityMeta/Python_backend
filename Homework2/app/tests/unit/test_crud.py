import pytest
from ... import crud
from ...database import ModelDb


@pytest.mark.parametrize(
    "score",
    [
        0.999,  # add model with set score
        None,  # add model with none score
        1.5,  # invalid score, 1.5 > 1.0
    ],
)
def test_add_model(named_model, db, score):
    # test for adding model where score must be in [0,1]
    named_model.score = score
    try:
        crud.add_model(named_model, db)
        assert score is None or (score >= 0.0 and score <= 1.0)
    except:
        assert not (score >= 0.0 and score <= 1.0)


@pytest.mark.parametrize(
    "id, if_get",
    [
        (1, True),  # model with none score
        (2, True),  # model with set score
        (3, False),  # model with this id does not exist
    ],
)
def test_get_model(models, db, id, if_get):
    # test for get model by id
    if_none = crud.get_model(id, db) is not None
    assert if_none == if_get


@pytest.mark.parametrize(
    "id, score",
    [
        (1, 0.5),  # update score of model with none score
        (2, 0.5),  # update score of model with set score
        (1, 1.5),  # update score of model by invalid score
        (3, 0.5),  # model with this id does not exist
    ],
)
def test_update_model(models, db, id, score):
    # test for updating model score by id
    try:
        db_model = crud.update_model(id, score, db)
        assert db_model.score == score
    except:
        assert not (score >= 0.0 and score <= 1.0) or id > len(db.query(ModelDb).all())


def test_get_max_score_0_cand(db):
    # test for getting models with max score where none of models was added
    try:
        crud.get_max_score(db)
        assert (
            False
        ), "Can not extract models with max score as none of the models was added"
    except:
        assert True


def test_get_max_score_cands_with_none_scores(
    models_max_score_cands_with_none_scores, db
):
    # test for getting models with max score where none of models has set score
    try:
        crud.get_max_score(db)
        assert False, "Can not extract models with max score as none of scores was set"
    except:
        assert True


def test_get_max_score_1_cand(models_max_score_1_cand, db):
    # test for getting models with max score where one model has max score
    db_models = crud.get_max_score(db)
    assert len(db_models) == 1


def test_get_max_score_2_cand(models_max_score_2_cand, db):
    # test for getting models with max score where more than one model has max score
    db_models = crud.get_max_score(db)
    assert len(db_models) == 2
