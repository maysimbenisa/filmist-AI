from fastapi import FastAPI
from backend.routes import recommend  # ⬅️ import your new route

app = FastAPI(title="FilmistAI API", version="1.0")

app.include_router(recommend.router)

@app.get("/")
def home():
    return {"message": "🎬 Welcome to FilmistAI — Phase 1 API"}
