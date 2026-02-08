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
st.set_page_config(
    page_title="Customer Support Assistant",
    page_icon="🎧",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
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
    vector_store = VectorStore(
        persist_dir=Config.CHROMA_PERSIST_DIR,
        collection_name=Config.COLLECTION_NAME
    )
    
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
    
    # Initialize agent
    agent = CustomerSupportAgent(vector_store, ticket_manager)
    
    return agent, None


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">Customer Support Assistant</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Powered by AI - {Config.COMPANY_NAME}</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = None
        st.session_state.error = None
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""
    
    # Sidebar - User Information
    with st.sidebar:
        st.header("User Information")
        st.session_state.user_name = st.text_input(
            "Your Name",
            value=st.session_state.user_name,
            placeholder="John Doe"
        )
        st.session_state.user_email = st.text_input(
            "Your Email",
            value=st.session_state.user_email,
            placeholder="john@example.com"
        )
        
        st.divider()
        
        st.header("Company Contact")
        st.write(f"**{Config.COMPANY_NAME}**")
        st.write(f"Email: {Config.COMPANY_EMAIL}")
        st.write(f"Phone: {Config.COMPANY_PHONE}")
        
        st.divider()
        
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            if st.session_state.agent:
                st.session_state.agent.clear_history()
            st.rerun()
    
    # Initialize system if not done
    if st.session_state.agent is None and st.session_state.error is None:
        with st.spinner("Initializing support system..."):
            agent, error = initialize_system()
            st.session_state.agent = agent
            st.session_state.error = error
    
    # Show error if initialization failed
    if st.session_state.error:
        st.error(st.session_state.error)
        st.info("Please check your configuration and try again.")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role):
            st.markdown(content)
    
    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent.process_message(
                    user_message=prompt,
                    user_name=st.session_state.user_name if st.session_state.user_name else None,
                    user_email=st.session_state.user_email if st.session_state.user_email else None
                )
                st.markdown(response)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
