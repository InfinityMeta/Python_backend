from pydantic import BaseModel


class ModelAdd(BaseModel):
    """
    schema for adding model to database
    """

    name: str
    score: float | None
