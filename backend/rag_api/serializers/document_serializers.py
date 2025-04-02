from rest_framework import serializers
from ..models import Document

class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_name', 'file_type', 'upload_date', 'chunk_count']

class DocumentUploadSerializer(serializers.Serializer):
    """Serializer for document upload."""
    title = serializers.CharField(max_length=255)
    file = serializers.FileField() 