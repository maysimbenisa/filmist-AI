import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("Missing OPENAI_API_KEY in .env file")

# Define the prompt template
prompt = ChatPromptTemplate.from_template(
    "I liked these movies: {movies}. Suggest 5 similar films and explain briefly why I'd enjoy each."
)

# Initialize the model
model = ChatOpenAI(
    model="gpt-4o-mini",  # fast, inexpensive, solid reasoning
    temperature=0.7,
    openai_api_key=openai_key,
)

# Combine prompt + model into a runnable chain
chain = prompt | model

def get_recommendations(movies: list[str]) -> str:
    """
    Given a list of movie titles, ask GPT to suggest similar movies.
    """
    movies_str = ", ".join(movies)
    response = chain.invoke({"movies": movies_str})
    return response.content
