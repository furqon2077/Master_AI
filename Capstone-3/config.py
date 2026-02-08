"""
Configuration management for Customer Support RAG System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Google Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL = "gemini-pro"
    
    # GitHub
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER")
    GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME")
    
    # Company Information
    COMPANY_NAME = os.getenv("COMPANY_NAME", "Customer Support")
    COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "support@company.com")
    COMPANY_PHONE = os.getenv("COMPANY_PHONE", "+1-800-000-0000")
    
    # ChromaDB
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/vector_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "support_documents")
    
    # Document Processing
    DOCUMENTS_DIR = "./data/documents"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Retrieval Settings
    TOP_K_RESULTS = 3
    SIMILARITY_THRESHOLD = 0.7
    
    # Agent Settings
    MAX_CONVERSATION_HISTORY = 10
    SYSTEM_PROMPT = f"""You are a helpful customer support assistant for {COMPANY_NAME}.

Your responsibilities:
1. Answer customer questions based on the provided documentation
2. Always cite your sources with the document name and page number
3. If you cannot find a relevant answer, suggest creating a support ticket
4. When asked about company information, provide: {COMPANY_NAME}, {COMPANY_EMAIL}, {COMPANY_PHONE}

When answering questions:
- Be clear, concise, and helpful
- Always include source citations in the format: [Document Name, Page X]
- If the information is not in the documents, be honest and suggest creating a support ticket

You have access to the following functions:
- search_documents: Search the knowledge base for information
- create_support_ticket: Create a support ticket when the user requests it or when you cannot find an answer
"""

# Validate required configuration
def validate_config():
    """Validate that required configuration is present"""
    errors = []
    
    if not Config.GOOGLE_API_KEY:
        errors.append("GOOGLE_API_KEY is not set")
    
    if not Config.GITHUB_TOKEN:
        errors.append("GITHUB_TOKEN is not set")
    
    if not Config.GITHUB_REPO_OWNER:
        errors.append("GITHUB_REPO_OWNER is not set")
    
    if not Config.GITHUB_REPO_NAME:
        errors.append("GITHUB_REPO_NAME is not set")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True
