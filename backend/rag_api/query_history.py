"""Query history module for the RAG API."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import QueryHistory
from .serializers import QueryHistorySerializer


class QueryHistoryView(APIView):
    """API view for retrieving query history."""
    
    def get(self, request):
        """Get all query history records."""
        query_history = QueryHistory.objects.all().order_by('-timestamp')
        serializer = QueryHistorySerializer(query_history, many=True)
        return Response(serializer.data)