from pydantic import BaseModel


class Advert(BaseModel):
    """Contract for advert."""

    id: int
    title: str
    text: str
    author_id: int
    published: bool
    moder_com: str | None


class User(BaseModel):
    """Contract for user."""

    id: int
    nickname: str | None = None
    email: str
