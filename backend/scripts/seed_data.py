"""
seed_data.py — Phase 1 Data Gathering for FilmistAI
----------------------------------------------------
Fetches movie metadata from TMDB and saves it as data/movies.jsonl
You can later use this JSONL file for embeddings or DB seeding.
"""

import os
import json
import time
import requests
from dotenv import load_dotenv
from pathlib import Path

# 1️⃣ Load your TMDB API key from .env
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# 2️⃣ Output file setup
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "movies.jsonl"

# 3️⃣ Fetch function for TMDB API
def fetch_movies(page: int):
    """Fetch one page of movies from TMDB (20 per page)."""
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": "false",
        "include_video": "false",
        "page": page,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["results"]

# 4️⃣ Simple cleaner — standardize field names
def clean_movie(m):
    """Normalize TMDB movie fields."""
    return {
        "movie_id": m["id"],
        "title": m.get("title") or m.get("name"),
        "overview": m.get("overview", ""),
        "genres": m.get("genre_ids", []),
        "release_date": m.get("release_date"),
        "popularity": m.get("popularity"),
        "vote_average": m.get("vote_average"),
        "vote_count": m.get("vote_count"),
        "language": m.get("original_language"),
        "poster_path": m.get("poster_path"),
    }

# 5️⃣ Main function — loops through many pages
def main(pages: int = 250):
    """
    Fetch and save ~5000 movies (20 per page × 250 pages).
    Adjust `pages` if you want fewer.
    """
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for page in range(1, pages + 1):
            data = fetch_movies(page)
            for movie in data:
                # Skip entries missing overview/title
                if not movie.get("overview") or not movie.get("title"):
                    continue
                clean = clean_movie(movie)
                f.write(json.dumps(clean, ensure_ascii=False) + "\n")
            print(f"✅ Page {page} done ({len(data)} movies)")
            time.sleep(0.25)  # be nice to API rate limits
    print(f"\n✅ Finished! Saved {pages*20} movies → {OUTPUT_FILE}")

if __name__ == "__main__":
    main(pages=250)
