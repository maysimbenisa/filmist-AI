@router.get("/similar/{movie_id}")
def similar_movies(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    # Retrieve its embedding and compare with others via cosine similarity
