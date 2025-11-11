"""
embedding_service.py — Phase 1 Semantic Embedding Generator for FilmistAI
---------------------------------------------------------------------------
Reads movies.jsonl and generates embeddings using a PyTorch model.
Outputs:
    data/embeddings.npy   → matrix of shape (N_movies, embedding_dim)
    data/ids.json         → matching list of movie IDs
"""

import os
import json
import numpy as np
from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 1️⃣ Load environment + model
load_dotenv()
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

print(f"🔧 Loading embedding model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)  # PyTorch under the hood

# 2️⃣ Input / Output paths
DATA_PATH = Path("data/movies.jsonl")
EMB_PATH = Path("data/embeddings.npy")
IDS_PATH = Path("data/ids.json")

# 3️⃣ Load your movies
with open(DATA_PATH, "r", encoding="utf-8") as f:
    movies = [json.loads(line) for line in f]

print(f"🎬 Loaded {len(movies)} movies for embedding.")

# 4️⃣ Prepare text for embedding
def make_text(movie):
    """Combine title + overview to form semantic input text."""
    return f"{movie['title']}. {movie.get('overview', '')}"

texts = [make_text(m) for m in movies]
movie_ids = [m["movie_id"] for m in movies]

# 5️⃣ Generate embeddings in batches
print("⚙️ Generating embeddings...")
embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

# 6️⃣ Save results
np.save(EMB_PATH, embeddings)
with open(IDS_PATH, "w", encoding="utf-8") as f:
    json.dump(movie_ids, f)

print(f"\n✅ Saved {embeddings.shape[0]} embeddings → {EMB_PATH}")
print(f"🆔 Saved movie ID list → {IDS_PATH}")
print(f"💡 Example vector shape: {embeddings.shape[1]} dimensions per movie")
