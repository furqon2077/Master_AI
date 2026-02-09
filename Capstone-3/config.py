"""
Configuration management for Customer Support RAG System
"""

from pathlib import Path
import os

# Optional imports (safe on Streamlit Cloud)
try:
    import streamlit as st
except ImportError:
    st = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_secret(key: str, default: str | None = None) -> str | None:
    """
    Unified secret loader:
    1. Streamlit secrets (Cloud)
    2. Environment variables (local / CI)
    3. Default fallback
    """
    if st and hasattr(st, "secrets") and key in st.secrets:
        return st.secrets[key]
    return os.getenv(key, default)


class Config:
    """Application configuration"""

    # ------------------------------------------------------------------
    # Base paths (ANCHOR EVERYTHING TO REPO ROOT)
    # ------------------------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent

    DATA_DIR = BASE_DIR / "data"
    DOCUMENTS_DIR = DATA_DIR / "documents"
    VECTOR_DB_DIR = DATA_DIR / "vector_db"

    # ------------------------------------------------------------------
    # OpenAI Configuration
    # ------------------------------------------------------------------
    OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS = 1000

    # ------------------------------------------------------------------
    # GitHub Configuration (Streamlit-safe)
    # ------------------------------------------------------------------
    GITHUB_TOKEN = get_secret("GITHUB_TOKEN")
    GITHUB_REPO_OWNER = get_secret("GITHUB_REPO_OWNER")
    GITHUB_REPO_NAME = get_secret("GITHUB_REPO_NAME")

    # ------------------------------------------------------------------
    # App Identity
    # ------------------------------------------------------------------
    COMPANY_NAME = get_secret("COMPANY_NAME", "Scripture Search")
    APP_TITLE = "Search God's Word in 3 Scripts"
    COMPANY_EMAIL = get_secret("COMPANY_EMAIL", "guidance@divinewisdom.com")
    COMPANY_PHONE = get_secret("COMPANY_PHONE", "+1-800-WISDOM-1")

    # ------------------------------------------------------------------
    # Vector Store (ChromaDB)
    # ------------------------------------------------------------------
    CHROMA_PERSIST_DIR = VECTOR_DB_DIR
    COLLECTION_NAME = get_secret("COLLECTION_NAME", "sacred_texts")

    # ------------------------------------------------------------------
    # Document Processing
    # ------------------------------------------------------------------
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # ------------------------------------------------------------------
    # Retrieval Settings
    # ------------------------------------------------------------------
    TOP_K_RESULTS = 5
    SIMILARITY_THRESHOLD = 0.6

    # ------------------------------------------------------------------
    # Agent Settings
    # ------------------------------------------------------------------
    MAX_CONVERSATION_HISTORY = 10

    SYSTEM_PROMPT = """You are a divine assistant dedicated to searching God's word across the three holy scripts (Torah, Bible, Quran).

Your Core Mission:
1. Search and retrieve wisdom from ALL three scripts when answering inquiries.
2. Provide specific version information for every citation.
3. Be EXTREMELY SENSITIVE to user feedback.

[... unchanged prompt ...]
"""


# ----------------------------------------------------------------------
# Configuration Validation
# ----------------------------------------------------------------------
def validate_config() -> bool:
    """Validate required configuration values"""
    errors = []

    if not Config.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is not set")

    if not Config.GITHUB_TOKEN:
        errors.append("GITHUB_TOKEN is not set")

    if not Config.GITHUB_REPO_OWNER:
        errors.append("GITHUB_REPO_OWNER is not set")

    if not Config.GITHUB_REPO_NAME:
        errors.append("GITHUB_REPO_NAME is not set")

    if not Config.DOCUMENTS_DIR.exists():
        errors.append(f"Documents directory not found: {Config.DOCUMENTS_DIR}")

    if errors:
        raise RuntimeError("Configuration errors:\n- " + "\n- ".join(errors))

    return True
