from fastapi import APIRouter
from typing import List
from ..langchain_recs import get_recommendations

# Create router instance
router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)

# POST endpoint to get AI movie recommendations
@router.post("/")
def recommend_movies(movies: List[str]):
    """
    Given a list of movie titles, return AI-generated recommendations.
    """
    recs = get_recommendations(movies)
    return {"recommendations": recs}
