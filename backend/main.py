from fastapi import FastAPI
from .database import Base, engine
from .routes import movies, recommend

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize the app
app = FastAPI(title="FilmistAI Backend")

# Include routers
app.include_router(movies.router)
app.include_router(recommend.router)

@app.get("/")
def root():
    return {"message": "FilmistAI backend is running 🎬"}
