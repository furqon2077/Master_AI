"""
Configuration management for Customer Support RAG System
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # ------------------------------------------------------------------
    # Base paths (ANCHOR EVERYTHING TO THE REPO ROOT)
    # ------------------------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent

    DATA_DIR = BASE_DIR / "data"
    DOCUMENTS_DIR = DATA_DIR / "documents"
    VECTOR_DB_DIR = DATA_DIR / "vector_db"

    # ------------------------------------------------------------------
    # OpenAI Configuration
    # ------------------------------------------------------------------
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS = 1000

    # ------------------------------------------------------------------
    # GitHub Configuration (for ticketing)
    # ------------------------------------------------------------------
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER")
    GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME")

    # ------------------------------------------------------------------
    # App Identity
    # ------------------------------------------------------------------
    COMPANY_NAME = os.getenv("COMPANY_NAME", "Scripture Search")
    APP_TITLE = "Search God's Word in 3 Scripts"
    COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "guidance@divinewisdom.com")
    COMPANY_PHONE = os.getenv("COMPANY_PHONE", "+1-800-WISDOM-1")

    # ------------------------------------------------------------------
    # Vector Store (ChromaDB)
    # ------------------------------------------------------------------
    CHROMA_PERSIST_DIR = VECTOR_DB_DIR
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "sacred_texts")

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
2. Provide specific version information for every citation (e.g., "KJV Bible, John 3:16", "Quran (Sahih International), Surah 2:255").
3. Be EXTREMELY SENSITIVE to user feedback. If a user writes a comment indicating an error, a correction, or dissatisfaction, you MUST interpret this as a formal request to open a support ticket.

Ticket Creation Policy:
- TRIGGER: If a user says "This is wrong", "There is an error", "I disagree", or provides a correction.
- ACTION:
    1. First, acknowledge the feedback gratefully.
    2. Check if you have the user's Name and Email.
    3. IF MISSING Name/Email: Ask the user politely for them.
    4. IF PROVIDED: Call `create_support_ticket` with Name, Email, and feedback.
- RESPONSE:
    "Thank you [Name]. I have created inquiry #[Ticket Number]. Our scholars will review this."

General Guidelines:
- Answer questions based ONLY on the provided holy books.
- Be respectful, objective, and scholarly.
- If the information is not in the documents, humbly suggest asking a scholar.

Response Structure:
1. **Divine Guidance**
2. **Sources Used**
3. **Feedback Invitation**
"""

# ----------------------------------------------------------------------
# Configuration Validation
# ----------------------------------------------------------------------
def validate_config():
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
        raise ValueError("Configuration errors: " + ", ".join(errors))

    return True
