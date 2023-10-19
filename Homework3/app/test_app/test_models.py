import pytest


@pytest.mark.parametrize(
    "sepal_length, sepal_width, petal_length, petal_width, target",
    [
        (5.1, 3.5, 1.4, 0.2, 0),  # Iris-setosa
        (7.0, 3.2, 4.7, 1.4, 1),  # Iris-versicolor
        (6.3, 3.3, 6.0, 2.5, 2),  # Iris-virginica
    ],
)

# test for correct work of iris_model
def test_iris_model(
    iris_model, sepal_length, sepal_width, petal_length, petal_width, target
):
    predict = iris_model.predict(
        [[sepal_length, sepal_width, petal_length, petal_width]]
    )
    assert predict[0] == target


@pytest.mark.parametrize(
    "bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex, Biscoe, Dream, Torgersen, target",
    [
        (39.3, 20.6, 190, 3650, 0, 0, 0, 1, 0),  # Adelie
        (46.5, 17.9, 192, 3500, 1, 0, 1, 0, 1),  # Chinstrap
        (46.1, 13.2, 211, 4500, 1, 1, 0, 0, 2),  # Gentoo
    ],
)

# test for correct work of penguins_model
def test_penguins_model(
    penguins_model,
    bill_length_mm,
    bill_depth_mm,
    flipper_length_mm,
    body_mass_g,
    sex,
    Biscoe,
    Dream,
    Torgersen,
    target,
):
    predict = penguins_model.predict(
        [
            [
                bill_length_mm,
                bill_depth_mm,
                flipper_length_mm,
                body_mass_g,
                sex,
                Biscoe,
                Dream,
                Torgersen,
            ]
        ]
    )
    assert predict[0] == target
