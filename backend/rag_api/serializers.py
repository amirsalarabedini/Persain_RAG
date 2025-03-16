from rest_framework import serializers
from .models import Document, QueryHistory

class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_name', 'file_type', 'upload_date', 'chunk_count']

class QueryHistorySerializer(serializers.ModelSerializer):
    """Serializer for QueryHistory model."""
    documents_retrieved = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = QueryHistory
        fields = ['id', 'query_text', 'response_text', 'timestamp', 'documents_retrieved']

class DocumentUploadSerializer(serializers.Serializer):
    """Serializer for document upload."""
    title = serializers.CharField(max_length=255)
    file = serializers.FileField()

class QuerySerializer(serializers.Serializer):
    """Serializer for query requests."""
    query = serializers.CharField()