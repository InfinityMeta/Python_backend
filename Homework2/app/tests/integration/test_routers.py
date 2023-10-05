import pytest


@pytest.mark.parametrize(
    "score, status_code",
    [
        (0.999, 201),  # add model with set score
        (None, 201),  # add model with none score
        (1.5, 400),  # invalid score, 1.5 > 1.0
    ],
)
def test_add_model(client, named_model, score, status_code):
    # test post request for adding model where score must be in [0,1]
    named_model.score = score
    response = client.post(
        "/models/", json={"name": named_model.name, "score": named_model.score}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "id, status_code",
    [
        (1, 200),  # model with none score
        (2, 200),  # model with set score
        (3, 404),  # model with this id does not exist
    ],
)
def test_get_model(client, models, id, status_code):
    # test get request for exctraction of model by id
    response = client.get(f"/models/{id}")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "id, status_code",
    [
        (1, 404),  # model with none score
        (2, 200),  # model with set score
        (3, 404),  # model with this id does not exist
    ],
)
def test_get_model_score(client, models, id, status_code):
    # test get request for exctraction of model score by id
    response = client.get(f"/models/{id}/score")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "id, score, status_code",
    [
        (1, 0.5, 200),  # update score of model with none score
        (2, 0.5, 200),  # update score of model with set score
        (2, 1.5, 400),  # update score of model by invalid score
        (3, 0, 404),  # model with this id does not exist
    ],
)
def test_update_model_score(client, models, id, score, status_code):
    # test put request for update of model score by id
    response = client.put(
        f"/models/{id}?score={score}", json={"id": id, "score": score}
    )
    assert response.status_code == status_code


def test_get_max_score_0_cand(client):
    # test get request for models with max score where none of models was added
    response = client.get("/models/max_score/")
    assert response.status_code == 404


def test_get_max_score_cands_with_none_scores(
    client, models_max_score_cands_with_none_scores
):
    # test get request for models with max score where none of models has set score
    response = client.get("/models/max_score/")
    assert response.status_code == 404


def test_get_max_score_1_cand(client, models_max_score_1_cand):
    # test get request for models with max score where one model has max score
    response = client.get("/models/max_score/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_max_score_2_cand(client, models_max_score_2_cand):
    # test get request for models with max score where more than one model has max score
    response = client.get("/models/max_score/")
    assert response.status_code == 200
    assert len(response.json()) == 2
