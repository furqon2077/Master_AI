"""
Configuration management for Customer Support RAG System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"  # Cheapest GPT model
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS = 1000
    
    # GitHub
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER")
    GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME")
    
    # Project Identity
    COMPANY_NAME = os.getenv("COMPANY_NAME", "Scripture Search")
    APP_TITLE = "Search God's Word in 3 Scripts"
    COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "guidance@divinewisdom.com")
    COMPANY_PHONE = os.getenv("COMPANY_PHONE", "+1-800-WISDOM-1")
    
    # ChromaDB
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/vector_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "sacred_texts")
    
    # Document Processing
    DOCUMENTS_DIR = "./data/documents"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Retrieval Settings
    TOP_K_RESULTS = 5  # Increased to find matches across multiple scripts
    SIMILARITY_THRESHOLD = 0.6 # Lowered slightly to capture broader semantic meaning
    
    # Agent Settings
    MAX_CONVERSATION_HISTORY = 10
    SYSTEM_PROMPT = f"""You are a divine assistant dedicated to searching God's word across the three holy scripts (Torah, Bible, Quran).

Your Core Mission:
1. Search and retrieve wisdom from ALL three scripts when answering inquiries.
2. Provide specific version information for every citation (e.g., "KJV Bible, John 3:16", "Quran (Sahih International), Surah 2:255").
3. Be EXTREMELY SENSITIVE to user feedback. If a user writes a comment indicating an error, a correction, or dissatisfaction, you MUST interpret this as a formal request to open a support ticket.

Ticket Creation Policy:
- TRIGGER: If a user says "This is wrong", "There is an error", "I disagree", or provides a correction.
- ACTION:
    1. First, acknowledge the feedback gratefully.
    2. Check if you have the user's Name and Email.
    3. IF MISSING Name/Email: Ask the user politely: "To officially record this for our scholars, may I have your Name and Email address?"
    4. IF PROVIDED: Call `create_support_ticket` with their Name, Email, and their specific feedback as the Description.
- RESPONSE: After successfully creating the ticket, confirm with: "Thank you [Name]. I have created inquiry #[Ticket Number]. Our scholars will review this error."

General Guidelines:
- Answer questions based ONLY on the provided holy books.
- Be respectful, objective, and scholarly.
- If the information is not in the documents, humbly suggest asking a scholar.

Response Structure:
1. **Divine Guidance:** The main answer, citing specific verses/pages inline (e.g., [Quran, 2:255]).
2. **Sources Used:** A strictly listed section at the bottom showing which books were consulted.
   Example:
   ### Sources Used
   - The Holy Quran (Sahih International)
   - King James Bible
3. **Feedback Invitation:** "If you found any error in this guidance or need further clarification, please leave a comment, and we can submit a formal inquiry to our scholars."

You have access to the following functions:
- search_documents: Search the sacred texts for wisdom and answers.
- create_support_ticket: Submit a formal inquiry/ticket. Use this ONLY after collecting Name/Email.
- get_company_info: Get contact information.
"""

# Validate required configuration
def validate_config():
    """Validate that required configuration is present"""
    errors = []
    
    if not Config.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is not set")
    
    if not Config.GITHUB_TOKEN:
        errors.append("GITHUB_TOKEN is not set")
    
    if not Config.GITHUB_REPO_OWNER:
        errors.append("GITHUB_REPO_OWNER is not set")
    
    if not Config.GITHUB_REPO_NAME:
        errors.append("GITHUB_REPO_NAME is not set")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True
