"""
vector_search.py — Phase 1 Semantic Search Engine for FilmistAI
----------------------------------------------------------------
Loads your movie embeddings and builds a FAISS index for fast similarity search.
Supports:
    - movie-to-movie similarity lookup
    - text-to-movie semantic search (using same embedding model)
Outputs:
    data/movies.index  → FAISS index file for fast queries
"""

import os
import json
import faiss
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 1️⃣ Load environment + paths
load_dotenv()
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
DATA_DIR = Path("data")
EMB_PATH = DATA_DIR / "embeddings.npy"
IDS_PATH = DATA_DIR / "ids.json"
INDEX_PATH = DATA_DIR / "movies.index"
MOVIES_PATH = DATA_DIR / "movies.jsonl"

# 2️⃣ Load your existing embeddings + IDs
print("🎬 Loading embeddings and movie IDs...")
embeddings = np.load(EMB_PATH)
with open(IDS_PATH, "r", encoding="utf-8") as f:
    movie_ids = json.load(f)
movies = [json.loads(l) for l in open(MOVIES_PATH, "r", encoding="utf-8")]

print(f"✅ Loaded {len(movies)} movies with {embeddings.shape[1]}-dim embeddings.")

# 3️⃣ Create or load FAISS index
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatIP(embedding_dim)  # cosine similarity (after normalization)
faiss.normalize_L2(embeddings)
index.add(embeddings)
faiss.write_index(index, str(INDEX_PATH))
print(f"💾 FAISS index built and saved → {INDEX_PATH}")

# 4️⃣ Load model for text queries
model = SentenceTransformer(MODEL_NAME)
print(f"🔧 Model loaded: {MODEL_NAME}")

# 5️⃣ Utility — map movie_id to its data
movie_map = {m["movie_id"]: m for m in movies}

# 6️⃣ Search functions
def search_similar_movies(movie_id: int, top_k: int = 5):
    """Find movies most similar to a given movie_id."""
    try:
        idx = movie_ids.index(movie_id)
    except ValueError:
        return f"❌ Movie ID {movie_id} not found."

    query_vec = embeddings[idx].reshape(1, -1)
    D, I = index.search(query_vec, top_k + 1)  # +1 to skip the movie itself
    results = []
    for i, score in zip(I[0][1:], D[0][1:]):  # skip first (self)
        m = movie_map[movie_ids[i]]
        results.append({"title": m["title"], "score": float(score), "overview": m["overview"]})
    return results


def search_by_text(query: str, top_k: int = 5):
    """Find movies semantically similar to a text query."""
    q_emb = model.encode([query], normalize_embeddings=True)
    D, I = index.search(q_emb, top_k)
    results = []
    for i, score in zip(I[0], D[0]):
        m = movie_map[movie_ids[i]]
        results.append({"title": m["title"], "score": float(score), "overview": m["overview"]})
    return results


# 7️⃣ Quick demo
if __name__ == "__main__":
    print("\n🎥 Example 1: Find movies similar to Inception")
    inception_id = next(m["movie_id"] for m in movies if m["title"].lower() == "inception")
    similar = search_similar_movies(inception_id, top_k=5)
    for r in similar:
        print(f"→ {r['title']}  (score={r['score']:.3f})")

    print("\n🎥 Example 2: Search by text — 'space survival and isolation'")
    text_results = search_by_text("space survival and isolation", top_k=5)
    for r in text_results:
        print(f"→ {r['title']}  (score={r['score']:.3f})")
