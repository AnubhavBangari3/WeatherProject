import os
from dotenv import load_dotenv

load_dotenv()

# DeepSeek


# LangSmith / LangChain
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "weather-pdf-agent")

# Weather
WEATHER_KEY = os.getenv("WEATHER_KEY")

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# PDF
PDF_PATH = os.getenv("PDF_PATH", "./data/knowledge.pdf")
