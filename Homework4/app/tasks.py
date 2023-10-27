import random
import time

import pandas as pd
from celery import Celery

ANECDOTS_PATH = "./app/datasets/anecdots.csv"
NUTRIENTS_PATH = "./app/datasets/nutrients.csv"

df_anecdots = pd.read_csv(ANECDOTS_PATH)
num_of_anecdots = len(df_anecdots)
df_nutrients = pd.read_csv(NUTRIENTS_PATH)

app = Celery(
    "celery_rabbitmq", broker="amqp://", backend="rpc://", include=["app.tasks"]
)


@app.task
def get_random_anecdot() -> str:
    """
    Returns random anecdot.

    Returns:
        str: random anecdot
    """
    print("Choosing an anecdot for you...")
    time.sleep(10)
    i = random.randint(0, num_of_anecdots - 1)
    return df_anecdots.iloc[i]["text"]


@app.task
def get_food_calories(food_name: str) -> str:
    """
    Count callories for a food.

    Args:
        food_name (str): name of food

    Returns:
        str: number of callories
    """
    cals = df_nutrients.query(f'Food == "{food_name}"')["Calories"].values
    if len(cals) == 0:
        return None
    print("Counting calories...")
    time.sleep(10)
    return cals[0]
