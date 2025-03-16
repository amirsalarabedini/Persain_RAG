from django.db import models

class Document(models.Model):
    """Model to track documents uploaded to the RAG system."""
    title = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    chunk_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class QueryHistory(models.Model):
    """Model to track user queries and responses."""
    query_text = models.TextField()
    response_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    documents_retrieved = models.ManyToManyField(Document, related_name='queries')
    
    def __str__(self):
        return self.query_text[:50] + '...' if len(self.query_text) > 50 else self.query_text