
# 🎥 FilmistAI
**Your personal cinephile consultant — powered by FastAPI + LangChain.**

FilmistAI is an AI-powered movie catalog and recommendation application that helps you log, rate, and discover films like a true film lover.
Describe what you like — and FilmistAI will find the next movie obsession for you. 🍿

---

## 🚀 Features

- 🎞️ Add and manage your personal movie catalog
- ⭐ Rate films across story, acting, cinematography, soundtrack, and rewatchability
- 🤖 Get personalized movie recommendations powered by **LangChain + GPT-4o**
- 🧠 Context-aware AI logic (ready for chat-based “cinephile cousin” in future phases)
- 🧩 Modular FastAPI architecture, easy to expand

---

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI (Python) |
| AI | LangChain 1.x + OpenAI GPT-4o-mini |
| Database | SQLite (PostgreSQL-ready) |
| Environment | Python 3.10+ |
| Frontend (coming soon) | SvelteKit |

---

## ⚙️ Setup

```bash
# Clone this repo
git clone https://github.com/<your-username>/filmist-ai.git
cd filmist-ai

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
