import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..services import QueryService
from ..serializers import QueryHistorySerializer, QuerySerializer

# Configure logging
logger = logging.getLogger(__name__)

class QueryView(APIView):
    """API view for querying the RAG system."""
    
    def post(self, request):
        """Process a query and return the response."""
        serializer = QuerySerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                query_text = serializer.validated_data['query']
                response_data = QueryService.process_query(query_text)
                return Response(response_data)
                
            except Exception as e:
                logger.error(f"Error processing query: {str(e)}")
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryHistoryView(APIView):
    """API view for retrieving query history."""
    
    def get(self, request):
        """Get all query history."""
        try:
            queries = QueryService.get_query_history()
            serializer = QueryHistorySerializer(queries, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching query history: {str(e)}")
            return Response(
                {"error": "Failed to fetch query history"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 