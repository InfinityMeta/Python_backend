from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from . import crud
from .database import get_db
from .schemas import ModelAdd


router = APIRouter()


@router.post("/models/")
def add_model(model: ModelAdd, db: Session = Depends(get_db)):
    """
    Add model with passed name and score (if it is set).

    Args:
        model (ModelAdd): data about model including name and score
        db (Session): database session

    Returns:
        dict: JSON response including model ID, name and score
    """
    try:
        model = crud.add_model(model, db)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model score must be in [0,1]",
        )
    content = {"id": model.id, "name": model.name, "score": model.score}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)


@router.get("/models/{id}")
def get_model(id: int, db: Session = Depends(get_db)):
    """
    Get model by ID.

    Args:
        id (int): model ID
        db (Session): database session

    Raises:
        HTTPException: if model is not found

    Returns:
        dict: JSON response including model ID, name and score
    """
    model = crud.get_model(id, db)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Model is not found"
        )
    content = {"id": model.id, "name": model.name, "score": model.score}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/models/{id}/score")
def get_model_score(id: int, db: Session = Depends(get_db)):
    """
    Get model score by ID.

    Args:
        id (int): model ID
        db (Session): database session

    Raises:
        HTTPException: if model is not found or score is not set

    Returns:
        dict: JSON response including model score
    """
    model = crud.get_model(id, db)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Model is not found"
        )
    if model.score is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Score is not set"
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"score": model.score})


@router.put("/models/{id}")
def update_model_score(id: int, score: float, db: Session = Depends(get_db)):
    """
    Get model by ID.

    Args:
        id (int): model ID
        score (float): model score
        db (Session): database session

    Raises:
        IntegrityError, HTTPException: if invalid score is provided

    Returns:
        dict: JSON response including model ID, name and score
    """
    model = crud.get_model(id, db)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Model is not found"
        )
    try:
        model = crud.update_model(id, score, db)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model score must be in [0,1]",
        )
    content = {"id": model.id, "name": model.name, "score": model.score}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/models/max_score/")
def get_max_score(db: Session = Depends(get_db)):
    """
    Get models with max score.

    Args:
        model_id (int): model ID
        db (Session): database session

    Raises:
        HTTPException: if none of the models is added or none of the scores is se

    Returns:
        List[ModelDb]: list of models with max score
    """
    models_max_score = crud.get_max_score(db)
    if len(models_max_score) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="None of the models is added"
        )
    if models_max_score[0].score is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="None of the scores is set"
        )
    return models_max_score
