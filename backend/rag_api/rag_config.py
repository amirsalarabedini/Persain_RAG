"""Configuration module for the RAG system integrated with Django settings."""

import os
from pathlib import Path
from django.conf import settings


class RAGConfig:
    """Configuration for the RAG system."""
    
    def __init__(self):
        """Initialize configuration from Django settings."""
        # API Keys
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.cohere_api_key = os.getenv("COHERE_API_KEY", "")
        
        # Vector DB Settings
        self.chroma_persist_directory = settings.RAG_SETTINGS['CHROMA_PERSIST_DIRECTORY']
        
        # Document Storage
        self.documents_directory = settings.RAG_SETTINGS['DOCUMENTS_DIRECTORY']
        
        # RAG Settings
        self.chunk_size = settings.RAG_SETTINGS['CHUNK_SIZE']
        self.chunk_overlap = settings.RAG_SETTINGS['CHUNK_OVERLAP']
        self.top_k_results = settings.RAG_SETTINGS['TOP_K_RESULTS']


# Create a global config instance
config = RAGConfig()


def validate_config():
    """Validate that all required configuration is present."""
    if not config.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is required but not set")
    if not config.cohere_api_key:
        raise ValueError("COHERE_API_KEY is required but not set")
    
    # Create chroma directory if it doesn't exist
    chroma_dir = Path(config.chroma_persist_directory)
    chroma_dir.mkdir(parents=True, exist_ok=True)
    
    # Create documents directory if it doesn't exist
    docs_dir = Path(config.documents_directory)
    docs_dir.mkdir(parents=True, exist_ok=True)