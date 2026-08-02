import os

# ==========================================
# Lenny Growth Assistant Configuration
# ==========================================

# Ollama
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434"
)

# Main local LLM
OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)

# Embedding model
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)

# SQLite database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./lenny_growth.db"
)

# Transcript directory
TRANSCRIPTS_DIR = os.getenv(
    "TRANSCRIPTS_DIR",
    "data/transcripts"
)

# Number of transcript results
TOP_K = int(
    os.getenv(
        "TOP_K",
        "5"
    )
)