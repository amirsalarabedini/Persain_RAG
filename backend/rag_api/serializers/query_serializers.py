from rest_framework import serializers
from ..models import QueryHistory
from .document_serializers import DocumentSerializer

class QueryHistorySerializer(serializers.ModelSerializer):
    """Serializer for QueryHistory model."""
    documents_retrieved = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = QueryHistory
        fields = ['id', 'query_text', 'response_text', 'timestamp', 'documents_retrieved']

class QuerySerializer(serializers.Serializer):
    """Serializer for query requests."""
    query = serializers.CharField() 