"""System information module for the RAG API."""

from rest_framework.views import APIView
from rest_framework.response import Response

from .vector_store import VectorStore
from .rag_config import config


class SystemInfoView(APIView):
    """API view for retrieving system information."""
    
    def get(self, request):
        """Get RAG system information."""
        # Get vector store stats
        vector_store = VectorStore()
        collection_stats = vector_store.get_collection_stats()
        
        # Compile system info
        system_info = {
            "vector_store": {
                "collection_name": collection_stats["collection_name"],
                "document_count": collection_stats["document_count"],
                "persist_directory": collection_stats["persist_directory"]
            },
            "config": {
                "chunk_size": config.chunk_size,
                "chunk_overlap": config.chunk_overlap,
                "top_k_results": config.top_k_results,
                "documents_directory": config.documents_directory
            }
        }
        
        return Response(system_info)