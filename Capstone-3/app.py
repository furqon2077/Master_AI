"""
Customer Support RAG System - Streamlit Web Application
"""
import streamlit as st
import os
from config import Config
from src.document_processor import DocumentProcessor
from src.chunking import TextChunker
from src.vector_store import VectorStore
from src.ticket_manager import TicketManager
from src.agent import CustomerSupportAgent

# Page configuration
# Page configuration
st.set_page_config(
    page_title="Divine Wisdom - Scripture Assistant",
    page_icon=None,
    layout="wide"
)

# Custom CSS for Forced Light Theme
st.markdown("""
<style>
    /* FORCED LIGHT MODE THEME */
    .stApp {
        background-color: #ffffff;
        color: #2c3e50;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6, p, div {
        color: #2c3e50 !important;
    }
    
    /* Message Bubbles */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1.5rem;
        font-family: 'Georgia', serif;
        line-height: 1.6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        color: #2c3e50;
    }
    
    .user-message {
        background-color: #f0f7ff; /* Crisp Light Blue */
        border: 1px solid #cce5ff;
        border-left: 5px solid #0056b3;
    }
    
    .assistant-message {
        background-color: #fffbf0; /* Warm Cream */
        border: 1px solid #f0e6cc;
        border-left: 5px solid #d4af37; /* Gold */
    }

    /* HEADER */
    .main-header {
        font-family: 'Georgia', serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        border-bottom: 3px solid #d4af37;
        padding-bottom: 1.5rem;
        color: #2c3e50 !important;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-family: 'Georgia', serif;
        font-size: 1.4rem;
        text-align: center;
        margin-bottom: 3rem;
        font-style: italic;
        color: #5d4037 !important;
        opacity: 0.9;
    }
    
    /* Input Areas */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #d4af37 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Initialize the RAG system components"""
    
    # Check if documents directory exists
    if not os.path.exists(Config.DOCUMENTS_DIR):
        return None, "Documents directory not found. Please create 'data/documents' and add PDF files."
    
    # Load documents
    doc_processor = DocumentProcessor(Config.DOCUMENTS_DIR)
    documents = doc_processor.load_all_documents()
    
    if not documents:
        return None, "No documents found. Please add PDF files to 'data/documents'."
    
    # Chunk documents
    chunker = TextChunker(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    chunked_docs = chunker.chunk_documents(documents)
    
    # Initialize vector store
    try:
        vector_store = VectorStore(
            persist_dir=Config.CHROMA_PERSIST_DIR,
            collection_name=Config.COLLECTION_NAME
        )
    except Exception as e:
        return None, f"Error initializing vector store: {str(e)}"
    
    # Check if we need to initialize the vector store
    if vector_store.get_collection_count() == 0:
        vector_store.add_documents(chunked_docs)
    
    # Initialize ticket manager
    try:
        ticket_manager = TicketManager(
            github_token=Config.GITHUB_TOKEN,
            repo_owner=Config.GITHUB_REPO_OWNER,
            repo_name=Config.GITHUB_REPO_NAME
        )
    except Exception as e:
        return None, f"Error initializing ticket manager: {str(e)}"
    
    # Validate OpenAI API Key
    if not Config.OPENAI_API_KEY:
        return None, "OpenAI API Key is missing. Please add OPENAI_API_KEY to your .env file."
        
    # Initialize agent
    try:
        agent = CustomerSupportAgent(vector_store, ticket_manager)
    except Exception as e:
        return None, f"Error initializing AI agent: {str(e)}"
    
    return agent, None


def main():
    """Main application"""
    
    # Header
    st.markdown(f'<div class="main-header">{Config.APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Comparing Wisdom across Torah, Bible, and Quran</div>', unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key Input
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Enter your OpenAI API Key to start the assistant",
            value=""
        )
        
        
        if api_key_input:
            Config.OPENAI_API_KEY = api_key_input
        
        # Remove contact info from UI as requested
        st.markdown("---")
        st.markdown("**Author: Furkat Sidikov**")
        
        st.divider()
        
        if st.button("Begin New Inquiry", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.agent:
                st.session_state.agent.clear_history()
            st.rerun()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = None
        st.session_state.error = None
    
    # Initialize system variables implicitly (no sidebar inputs)
    if "user_name" not in st.session_state:
        st.session_state.user_name = "Guest"
    
    if "user_email" not in st.session_state:
        st.session_state.user_email = "guest@example.com"
    
    # Initialize system if not done
    if st.session_state.agent is None and st.session_state.error is None:
        with st.spinner("Preparing the wisdom repository..."):
            agent, error = initialize_system()
            st.session_state.agent = agent
            st.session_state.error = error
    
    # Show error if initialization failed
    if st.session_state.error:
        st.error(st.session_state.error)
        st.info("Please check your configuration and try again.")
        return
    
    # Display chat messages with a centered container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
            with st.chat_message(role):
                st.markdown(content)
    
    # Input area in the middle of the page (not fixed at bottom)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create a form for input to allow "Enter" to submit
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_input(
                "Seek wisdom from the texts...",
                placeholder="Ask your question here...",
                key="user_input_widget",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("Ask", use_container_width=True)
    
    if submit_button and user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Rerun to show user message immediately
        st.rerun()
        
    # Generate response if last message is from user
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Consulting the sacred texts..."):
                response = st.session_state.agent.process_message(
                    user_message=st.session_state.messages[-1]["content"],
                    user_name=st.session_state.user_name if st.session_state.user_name else None,
                    user_email=st.session_state.user_email if st.session_state.user_email else None
                )
                st.markdown(response)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
