from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from ..database import Base, get_db
from ..main import app
from .. import crud
from ..schemas import ModelAdd


TEST_DATABASE_URL = "sqlite:///./app/tests/test_models_database.db"


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    connection.begin()
    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def named_model():
    return ModelAdd(name="Inception-V3")


@pytest.fixture
def named_scored_model():
    return ModelAdd(name="Inception-V3", score=0.5)


@pytest.fixture
def models(db, named_model, named_scored_model):
    crud.add_model(named_model, db)
    crud.add_model(named_scored_model, db)


@pytest.fixture
def models_max_score_cands_with_none_scores(db, named_model):
    crud.add_model(named_model, db)
    crud.add_model(named_model, db)


@pytest.fixture
def models_max_score_1_cand(db, named_model):
    named_model.score = 0.5
    crud.add_model(named_model, db)
    named_model.score = 0.7
    crud.add_model(named_model, db)


@pytest.fixture
def models_max_score_2_cand(db, named_model):
    named_model.score = 0.5
    crud.add_model(named_model, db)
    named_model.score = 0.7
    crud.add_model(named_model, db)
    named_model.score = 0.9
    crud.add_model(named_model, db)
    crud.add_model(named_model, db)
