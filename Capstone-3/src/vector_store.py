"""Vector store implementation using ChromaDB"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import logging
from src.document_processor import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    """Manage document embeddings and retrieval using ChromaDB"""
    
    def __init__(self, persist_dir: str, collection_name: str):
        """
        Initialize the vector store
        
        Args:
            persist_dir: Directory to persist the ChromaDB database
            collection_name: Name of the collection
        """
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        logger.info("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("Embedding model loaded")
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Customer support documents"}
        )
    
    def add_documents(self, documents: List[Document]):
        """
        Add documents to the vector store
        
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            logger.warning("No documents to add")
            return
        
        logger.info(f"Adding {len(documents)} documents to vector store...")
        
        # Prepare data for ChromaDB
        ids = []
        texts = []
        metadatas = []
        
        for idx, doc in enumerate(documents):
            doc_id = f"doc_{idx}_{doc.metadata.get('source', 'unknown')}_{doc.metadata.get('page', 0)}"
            
            ids.append(doc_id)
            texts.append(doc.content)
            
            # Prepare metadata (ChromaDB requires simple types)
            metadata = {
                "source": str(doc.metadata.get('source', 'unknown')),
                "page": int(doc.metadata.get('page', 0)),
                "chunk": int(doc.metadata.get('chunk', 0))
            }
            metadatas.append(metadata)
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True).tolist()
        
        # Add to ChromaDB
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        
        logger.info(f"Successfully added {len(documents)} documents to vector store")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of search results with documents and metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        
        if results['documents'] and results['documents'][0]:
            for idx in range(len(results['documents'][0])):
                result = {
                    'content': results['documents'][0][idx],
                    'metadata': results['metadatas'][0][idx],
                    'distance': results['distances'][0][idx] if 'distances' in results else None
                }
                formatted_results.append(result)
        
        return formatted_results
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection"""
        return self.collection.count()
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "Customer support documents"}
        )
        logger.info("Collection cleared")
    
    def initialize_from_documents(self, documents: List[Document], clear_existing: bool = False):
        """
        Initialize the vector store from a list of documents
        
        Args:
            documents: List of documents to index
            clear_existing: Whether to clear existing documents first
        """
        if clear_existing:
            self.clear_collection()
        
        self.add_documents(documents)
