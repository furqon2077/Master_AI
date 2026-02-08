"""Text chunking utilities for document processing"""

from typing import List
from src.document_processor import Document


class TextChunker:
    """
    Split documents into manageable chunks while preserving metadata.
    Designed to be safe for embedding models and vector databases.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize the text chunker.

        Args:
            chunk_size: Maximum number of characters per chunk
            chunk_overlap: Number of overlapping characters between chunks
        """
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, document: Document) -> List[Document]:
        """
        Split a single document into smaller chunks.

        Args:
            document: Document to chunk

        Returns:
            List of chunked Documents with preserved metadata
        """
        text = document.content or ""
        text = text.strip()

        if not text:
            return []

        # Small document → return as-is
        if len(text) <= self.chunk_size:
            return [document]

        chunks: List[Document] = []
        start = 0
        chunk_num = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + self.chunk_size, text_length)

            # Try to break at a sentence or newline boundary
            if end < text_length:
                for i in range(end, max(start + self.chunk_size // 2, start), -1):
                    if text[i - 1:i + 1] in {". ", "! ", "? ", "\n"}:
                        end = i
                        break

            # Extract and hard-cap chunk text
            chunk_text = text[start:end].strip()
            chunk_text = chunk_text[:self.chunk_size]

            if chunk_text:
                chunk_metadata = dict(document.metadata or {})
                chunk_metadata["chunk"] = chunk_num

                chunks.append(
                    Document(
                        content=chunk_text,
                        metadata=chunk_metadata
                    )
                )
                chunk_num += 1

            # Move start forward safely (avoid infinite loops)
            next_start = end - self.chunk_overlap
            if next_start <= start:
                break
            start = next_start

        return chunks

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Chunk multiple documents.

        Args:
            documents: List of documents to chunk

        Returns:
            Flattened list of all chunked documents
        """
        all_chunks: List[Document] = []

        for doc in documents:
            all_chunks.extend(self.chunk_document(doc))

        return all_chunks
