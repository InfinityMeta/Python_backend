import pytest


@pytest.mark.parametrize(
    "sepal_length, sepal_width, petal_length, petal_width, status_code",
    [
        (5.1, 3.5, 1.4, 0.2, 200),  # Ok
        (-5.1, 3.5, 1.4, 0.2, 400),  # sepal_length <0
        (5.1, -3.5, 1.4, 0.2, 400),  #  sepal_width <0
        (5.1, 3.5, -1.4, 0.2, 400),  #  petal_length <0
        (5.1, 3.5, 1.4, -0.2, 400),  #  petal_width <0
    ],
)

# test for correct prediction of iris_model
def test_iris_prediction(
    client, sepal_length, sepal_width, petal_length, petal_width, status_code
):
    response = client.get(
        f"/iris/prediction?sepal_length={sepal_length}&sepal_width={sepal_width}&petal_length={petal_length}&petal_width={petal_width}",
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex, status_code",
    [
        ("Torgersen", 39.3, 20.6, 190, 3650, "Male", 200),  # Ok
        ("Magascar", 39.3, 20.6, 190, 3650, "Male", 400),  # Incorrect island
        ("Torgersen", -39.3, 20.6, 190, 3650, "Male", 400),  # bill_length_mm <0
        ("Torgersen", 39.3, -20.6, 190, 3650, "Male", 400),  # bill_depth_mm <0
        ("Torgersen", 39.3, 20.6, -190, 3650, "Male", 400),  # flipper_length_mm <0
        ("Torgersen", 39.3, 20.6, 190, -3650, "Male", 400),  # bill_length_mm <0
        ("Torgersen", 39.3, 20.6, 190, -3650, "Avg", 400),  # Incorrect sex
    ],
)

# test for correct prediction of penguins_model
def test_penguins_prediction(
    client,
    island,
    bill_length_mm,
    bill_depth_mm,
    flipper_length_mm,
    body_mass_g,
    sex,
    status_code,
):
    response = client.get(
        f"/penguins/prediction?island={island}&bill_length_mm={bill_length_mm}&bill_depth_mm={bill_depth_mm}&flipper_length_mm={flipper_length_mm}&body_mass_g={body_mass_g}&sex={sex}",
    )
    assert response.status_code == status_code
