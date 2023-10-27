import time

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from .tasks import get_food_calories, get_random_anecdot

router = APIRouter()


@router.get("/")
def read_root():
    """
    Returns welcoming message.

    Returns:
        str: "Welcome to our service! Here you can fetch random anecdot or learn about food calories"
    """
    return {
        "message": "Welcome to our service! Here you can fetch random anecdot or learn about food calories"
    }


@router.get("/anecdots/")
async def get_anecdot() -> str:
    """
    Returns JSON response with random anecdot.

    Returns:
        dict: JSON response including random anecdot
    """
    anecdot = get_random_anecdot.delay()
    time.sleep(15)
    content = {"Anecdot": anecdot.get()}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/calories/{food_name}")
async def learn_calories(food_name: str) -> str:
    """
    Returns JSON response with callories counted for food.

    Args:
        food_name (str): name of food

    Returns:
        dict: JSON response including counted callories
    """
    calories = get_food_calories.delay(food_name)
    time.sleep(15)
    if calories is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=None)
    content = {"Anecdot": calories.get()}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
