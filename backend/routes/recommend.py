"""
recommend.py — Phase 1 FastAPI route for FilmistAI
--------------------------------------------------
Connects the vector search system to FastAPI, enabling live semantic search.
"""

from fastapi import APIRouter, Query, HTTPException
from backend.vector_search import search_by_text, search_similar_movies

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

@router.get("/")
def recommend_movies(query: str = Query(..., description="Search movies semantically")):
    """
    Find movies related to a free-text query.
    Example:
        /recommend?query=space+exploration+and+isolation
    """
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    results = search_by_text(query)
    if not results:
        raise HTTPException(status_code=404, detail="No matches found.")
    return {"query": query, "results": results}


@router.get("/similar/{movie_id}")
def recommend_similar(movie_id: int, top_k: int = Query(5, ge=1, le=20)):
    """
    Find movies similar to another movie by ID.
    Example:
        /recommend/similar/27205  (Inception)
    """
    results = search_similar_movies(movie_id, top_k=top_k)
    if isinstance(results, str):
        raise HTTPException(status_code=404, detail=results)
    return {"movie_id": movie_id, "results": results}
