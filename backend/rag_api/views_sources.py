"""Views for sources-only retrieval in the RAG system."""

import logging
from pathlib import Path

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Document
from .serializers import QuerySerializer

# Import local RAG system components
from .embedding import EmbeddingGenerator
from .vector_store import VectorStore

# Configure logging
logger = logging.getLogger(__name__)


class QuerySourcesView(APIView):
    """API view for retrieving only the sources for a query without generating a response."""
    
    def post(self, request):
        """Process a query and return only the relevant sources."""
        serializer = QuerySerializer(data=request.data)
        
        if serializer.is_valid():
            query_text = serializer.validated_data['query']
            
            try:
                # Initialize RAG components
                embedding_generator = EmbeddingGenerator()
                vector_store = VectorStore()
                
                logger.info(f"Processing query for sources only: {query_text[:50]}...")
                
                # Generate query embedding
                query_embedding = embedding_generator.generate_query_embedding(query_text)
                logger.info("Generated query embedding")
                
                # Search for relevant documents
                search_results = vector_store.search(query_embedding)
                logger.info(f"Found {len(search_results.get('documents', [[]])[0])} relevant document chunks")
                
                # Format response with only sources
                response_data = {
                    "query": query_text,
                    "sources": [
                        {
                            "content": doc[:200] + "..." if len(doc) > 200 else doc,
                            "metadata": metadata
                        }
                        for doc, metadata in zip(
                            search_results.get("documents", [[]])[0],
                            search_results.get("metadatas", [[]])[0]
                        )
                    ]
                }
                
                return Response(response_data)
                
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)