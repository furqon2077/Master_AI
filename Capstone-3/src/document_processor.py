"""Document processing module for PDF parsing and text extraction"""
import os
from typing import List, Dict
from PyPDF2 import PdfReader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Document:
    """Represents a document with content and metadata"""
    
    def __init__(self, content: str, metadata: Dict[str, any]):
        self.content = content
        self.metadata = metadata
    
    def __repr__(self):
        return f"Document(source={self.metadata.get('source')}, page={self.metadata.get('page')})"


class DocumentProcessor:
    """Process and load documents from various sources"""
    
    def __init__(self, documents_dir: str):
        self.documents_dir = documents_dir
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """
        Load a PDF file and extract text with page numbers
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of Document objects, one per page
        """
        documents = []
        
        try:
            reader = PdfReader(file_path)
            filename = os.path.basename(file_path)
            
            logger.info(f"Loading PDF: {filename} ({len(reader.pages)} pages)")
            
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                
                if text.strip():  # Only include pages with content
                    doc = Document(
                        content=text,
                        metadata={
                            "source": filename,
                            "page": page_num,
                            "file_path": file_path,
                            "total_pages": len(reader.pages)
                        }
                    )
                    documents.append(doc)
            
            logger.info(f"Extracted {len(documents)} pages from {filename}")
            
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {str(e)}")
            raise
        
        return documents
    
    def load_all_documents(self) -> List[Document]:
        """
        Load all PDF documents from the documents directory
        
        Returns:
            List of all Document objects from all PDFs
        """
        all_documents = []
        
        if not os.path.exists(self.documents_dir):
            logger.warning(f"Documents directory does not exist: {self.documents_dir}")
            return all_documents
        
        pdf_files = [f for f in os.listdir(self.documents_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.documents_dir}")
            return all_documents
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in pdf_files:
            file_path = os.path.join(self.documents_dir, pdf_file)
            documents = self.load_pdf(file_path)
            all_documents.extend(documents)
        
        logger.info(f"Total documents loaded: {len(all_documents)}")
        
        return all_documents
    
    def get_document_stats(self) -> Dict[str, any]:
        """
        Get statistics about the document collection
        
        Returns:
            Dictionary with document statistics
        """
        if not os.path.exists(self.documents_dir):
            return {"error": "Documents directory does not exist"}
        
        pdf_files = [f for f in os.listdir(self.documents_dir) if f.endswith('.pdf')]
        
        stats = {
            "total_files": len(pdf_files),
            "files": []
        }
        
        for pdf_file in pdf_files:
            file_path = os.path.join(self.documents_dir, pdf_file)
            try:
                reader = PdfReader(file_path)
                stats["files"].append({
                    "name": pdf_file,
                    "pages": len(reader.pages)
                })
            except Exception as e:
                logger.error(f"Error reading {pdf_file}: {str(e)}")
        
        return stats
