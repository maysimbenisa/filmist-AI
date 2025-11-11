# backend/main.py
from fastapi import FastAPI
from backend.routes import movies, recommend
from backend.database import Base, engine
from backend import models

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(title="FilmistAI 🎬", version="1.0")

# Include routes
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendations"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FilmistAI 🎬"}
