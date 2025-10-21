from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database

# Create router instance
router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

# Database session dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET: list all movies
@router.get("/", response_model=list[schemas.Movie])
def list_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()

# POST: add a new movie
@router.post("/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
