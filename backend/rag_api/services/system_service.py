import logging
from ..vector_store import VectorStore
from ..rag_config import config

# Configure logging
logger = logging.getLogger(__name__)

class SystemService:
    """Service for system-related operations."""
    
    @staticmethod
    def get_system_info():
        """Get RAG system information."""
        try:
            vector_store = VectorStore()
            stats = vector_store.get_collection_stats()
            
            return {
                "document_count": stats["document_count"],
                "collection_name": stats["collection_name"],
                "persist_directory": stats["persist_directory"],
                "chunk_size": config.chunk_size,
                "chunk_overlap": config.chunk_overlap,
                "top_k_results": config.top_k_results
            }
        except Exception as e:
            logger.error(f"Error getting system info: {str(e)}")
            raise 