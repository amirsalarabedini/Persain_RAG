"""Vector database module for the RAG system using ChromaDB."""

from typing import List, Dict, Any, Optional, Union
import chromadb
from chromadb.config import Settings
from tqdm import tqdm

from .rag_config import config
from .document_processor import DocumentChunk


class VectorStore:
    """Vector database for storing and retrieving document embeddings."""
    
    def __init__(self, persist_directory: Optional[str] = None, collection_name: str = "documents"):
        """Initialize the vector store with persistence settings."""
        self.persist_directory = persist_directory or config.chroma_persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
    
    def add_documents(self, embedded_chunks: Dict[str, Any]) -> None:
        """Add document embeddings to the vector store."""
        # Add documents in batches to avoid memory issues
        batch_size = 100
        total_docs = len(embedded_chunks["ids"])
        
        for i in tqdm(range(0, total_docs, batch_size), desc="Adding to vector store"):
            end_idx = min(i + batch_size, total_docs)
            self.collection.add(
                ids=embedded_chunks["ids"][i:end_idx],
                embeddings=embedded_chunks["embeddings"][i:end_idx],
                metadatas=embedded_chunks["metadatas"][i:end_idx],
                documents=embedded_chunks["documents"][i:end_idx]
            )
    
    def search(self, query_embedding: List[float], top_k: Optional[int] = None) -> Dict[str, Any]:
        """Search for similar documents using a query embedding."""
        top_k = top_k or config.top_k_results
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "documents", "distances"]
        )
        
        return results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count,
            "persist_directory": self.persist_directory
        }
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        self.client.delete_collection(name=self.collection_name)
        # Recreate an empty collection
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
    
    def get_all_documents(self) -> Dict[str, Any]:
        """Get all documents from the collection.
        
        Returns:
            Dict with ids, documents, metadatas, and embeddings.
        """
        # Get collection count
        count = self.collection.count()
        
        if count == 0:
            return {
                "ids": [],
                "documents": [],
                "metadatas": [],
                "embeddings": []
            }
        
        # Get all documents
        results = self.collection.get(
            include=["metadatas", "documents", "embeddings"]
        )
        
        return results
    
    def update_document_metadata(self, document_id: str, metadata: Dict[str, Any]) -> None:
        """Update metadata for a specific document.
        
        Args:
            document_id: The ID of the document to update
            metadata: The new metadata to set
        """
        # Get the current document to preserve other fields
        current = self.collection.get(
            ids=[document_id],
            include=["metadatas", "documents", "embeddings"]
        )
        
        if not current["ids"]:
            raise ValueError(f"Document with ID {document_id} not found")
        
        # Update metadata (merge with existing metadata)
        current_metadata = current["metadatas"][0]
        updated_metadata = {**current_metadata, **metadata}
        
        # Update the document
        self.collection.update(
            ids=[document_id],
            metadatas=[updated_metadata]
        )