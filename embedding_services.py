from sentence_transformers import SentenceTransformer
import numpy as np
from .database import SessionLocal
from .models import Movie, MovieEmbedding

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings():
    db = SessionLocal()
    movies = db.query(Movie).all()
    for movie in movies:
        text = f"{movie.title}. {movie.description or ''}"
        emb = model.encode(text)
        db.add(MovieEmbedding(movie_id=movie.id, embedding=emb.tolist()))
    db.commit()
    db.close()
