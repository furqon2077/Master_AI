"""
Initialize the vector database with documents
Run this script once after adding PDF documents to data/documents
"""
import os
from config import Config
from src.document_processor import DocumentProcessor
from src.chunking import TextChunker
from src.vector_store import VectorStore


def main():
    print("=" * 60)
    print("Customer Support RAG System - Initialization")
    print("=" * 60)
    
    # Check documents directory
    if not os.path.exists(Config.DOCUMENTS_DIR):
        print(f"\nError: Documents directory not found: {Config.DOCUMENTS_DIR}")
        print("Please create the directory and add PDF files.")
        return
    
    # Initialize document processor
    print(f"\n1. Loading documents from: {Config.DOCUMENTS_DIR}")
    doc_processor = DocumentProcessor(Config.DOCUMENTS_DIR)
    
    # Get document stats
    stats = doc_processor.get_document_stats()
    print(f"\nFound {stats['total_files']} PDF files:")
    for file_info in stats['files']:
        print(f"  - {file_info['name']}: {file_info['pages']} pages")
    
    # Load all documents
    print("\n2. Loading and parsing PDF documents...")
    documents = doc_processor.load_all_documents()
    print(f"Loaded {len(documents)} document pages")
    
    # Chunk documents
    print("\n3. Chunking documents...")
    chunker = TextChunker(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    chunked_docs = chunker.chunk_documents(documents)
    print(f"Created {len(chunked_docs)} chunks")
    
    # Initialize vector store
    print("\n4. Initializing vector database...")
    vector_store = VectorStore(
        persist_dir=Config.CHROMA_PERSIST_DIR,
        collection_name=Config.COLLECTION_NAME
    )
    
    # Add documents
    print("\n5. Adding documents to vector store...")
    vector_store.initialize_from_documents(chunked_docs, clear_existing=True)
    
    print(f"\n6. Vector store initialized with {vector_store.get_collection_count()} chunks")
    
    print("\n" + "=" * 60)
    print("Initialization complete!")
    print("=" * 60)
    print("\nYou can now run the application:")
    print("  streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
