import joblib
import pytest
from app.gateway.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def iris_model():
    path = "app/models/iris/iris_model.pickle"
    iris_model = joblib.load(path)
    return iris_model


@pytest.fixture
def penguins_model():
    path = "app/models/penguins/penguins_model.pickle"
    penguins_model = joblib.load(path)
    return penguins_model


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c
