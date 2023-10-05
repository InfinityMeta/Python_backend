from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import ModelDb
from .schemas import ModelAdd


def add_model(model: ModelAdd, db: Session):
    """
    Add model with passed name and score (if it is set) to database.

    Args:
        model (ModelAdd): data about model including name and score
        db (Session): database session

    Returns:
        db_model (ModelDb): model including ID, name, score
    """
    db_model = ModelDb(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def get_model(model_id: int, db: Session):
    """
    Get model by id.

    Args:
        model_id (int): model ID
        db (Session): database session

    Returns:
        db_model (ModelDb): model including ID, name, score
    """
    db_model = db.query(ModelDb).filter(ModelDb.id == model_id).first()
    return db_model


def update_model(model_id: int, model_score: float, db: Session):
    """
    Update model score by id.

    Args:
        model_id (int): model ID
        model_score (float): model score
        db (Session): database session

    Returns:
        db_model (ModelDb): model including ID, name, score
    """
    db.query(ModelDb).filter(ModelDb.id == model_id).update({"score": model_score})
    db.commit()
    db_model = get_model(model_id, db)
    db.refresh(db_model)
    return db_model


def get_max_score(db: Session):
    """
    Get models with max score.

    Args:
        db (Session): database session

    Returns:
        db_models (List[ModelDb]): list of models with max score
    """
    max_score = db.query(func.max(ModelDb.score)).scalar()
    db_models = db.query(ModelDb).filter(ModelDb.score == max_score).all()
    return db_models
