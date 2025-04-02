from django.db import models
from .document import Document

class QueryHistory(models.Model):
    """Model to track user queries and responses."""
    query_text = models.TextField()
    response_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    documents_retrieved = models.ManyToManyField(Document, related_name='queries')
    
    def __str__(self):
        return self.query_text[:50] + '...' if len(self.query_text) > 50 else self.query_text 