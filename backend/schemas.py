from pydantic import BaseModel
from typing import List

# --- Rating Schema ---
class RatingBase(BaseModel):
    story: float
    acting: float
    cinematography: float
    soundtrack: float
    rewatchability: float


# --- Movie Schema ---
class MovieBase(BaseModel):
    title: str
    year: int
    genre: str
    director: str
    actors: str


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    ratings: List[RatingBase] = []

    class Config:
        orm_mode = True
