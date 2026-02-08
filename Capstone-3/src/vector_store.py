import uuid
from math import ceil

def add_documents(self, documents: List[Document], batch_size: int = 4000):
    """
    Add documents to the vector store in safe batches
    """
    if not documents:
        logger.warning("No documents to add")
        return

    total_docs = len(documents)
    logger.info(f"Adding {total_docs} documents to vector store (batch_size={batch_size})")

    for start in range(0, total_docs, batch_size):
        end = start + batch_size
        batch = documents[start:end]

        logger.info(
            f"Processing batch {start // batch_size + 1}/"
            f"{ceil(total_docs / batch_size)} "
            f"({len(batch)} documents)"
        )

        texts = []
        metadatas = []
        ids = []

        for doc in batch:
            texts.append(doc.page_content)  # ✅ consistent with your chunker

            metadatas.append({
                "source": str(doc.metadata.get("source", "unknown")),
                "page": int(doc.metadata.get("page", 0)),
                "chunk": int(doc.metadata.get("chunk", 0)),
            })

            # ✅ globally unique, Streamlit-safe
            ids.append(str(uuid.uuid4()))

        # Generate embeddings for this batch only
        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=False
        )

        # Add batch to ChromaDB
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

    logger.info(f"Successfully added {total_docs} documents to vector store")