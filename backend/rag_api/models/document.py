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