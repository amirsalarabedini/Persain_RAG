"""Embedding module for the RAG system using Cohere API."""

import asyncio
import time
from typing import List, Dict, Any, Optional, Union, Tuple
import cohere
import numpy as np
from tqdm import tqdm
import httpx
import ssl
import logging

from .rag_config import config
from .document_processor import DocumentChunk

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generates embeddings for document chunks using Cohere API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "embed-english-v3.0", max_retries: int = 5):
        """Initialize the embedding generator with API key and model."""
        self.api_key = api_key or config.cohere_api_key
        self.model = model
        self.max_retries = max_retries
        self.client = cohere.Client(api_key=self.api_key)
        
        # Configure SSL context for better compatibility
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type="search_document"
        )
        return response.embeddings[0]
    
    def _call_with_retry(self, func, *args, **kwargs) -> Any:
        """Call a function with retry logic for handling connection errors."""
        retry_count = 0
        last_exception = None
        
        while retry_count < self.max_retries:
            try:
                return func(*args, **kwargs)
            except (httpx.ReadError, httpx.ConnectError, httpx.TimeoutException, ssl.SSLError) as e:
                retry_count += 1
                wait_time = 2 ** retry_count  # Exponential backoff
                last_exception = e
                
                logger.warning(f"Connection error on attempt {retry_count}/{self.max_retries}: {str(e)}")
                logger.info(f"Retrying in {wait_time} seconds...")
                
                time.sleep(wait_time)
            except Exception as e:
                # For non-connection errors, don't retry
                logger.error(f"Non-connection error: {str(e)}")
                raise
        
        # If we've exhausted retries, raise the last exception
        logger.error(f"Failed after {self.max_retries} retries. Last error: {str(last_exception)}")
        raise last_exception
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts in batches with retry logic."""
        # Cohere has rate limits, so we'll process in batches
        batch_size = 96  # Cohere's recommended batch size
        all_embeddings = []
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Generating embeddings"):
            batch_texts = texts[i:i + batch_size]
            
            try:
                # Use retry logic for the API call
                response = self._call_with_retry(
                    self.client.embed,
                    texts=batch_texts,
                    model=self.model,
                    input_type="search_document"
                )
                all_embeddings.extend(response.embeddings)
            except Exception as e:
                logger.error(f"Failed to generate embeddings for batch {i//batch_size + 1}: {str(e)}")
                # Return empty embeddings for this batch to allow partial processing
                logger.warning("Using zero vectors as fallback for failed embeddings")
                # Create zero vectors with the same dimensions as the model (1024 for embed-english-v3.0)
                embedding_dim = 1024
                for _ in range(len(batch_texts)):
                    all_embeddings.append([0.0] * embedding_dim)
        
        return all_embeddings
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a search query with retry logic."""
        try:
            response = self._call_with_retry(
                self.client.embed,
                texts=[query],
                model=self.model,
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {str(e)}")
            logger.warning("Using zero vector as fallback for query embedding")
            # Return a zero vector with the same dimensions as the model
            return [0.0] * 1024  # 1024 is the dimension for embed-english-v3.0
    
    async def generate_embeddings_async(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings asynchronously for better performance."""
        # This is a placeholder for async implementation
        # Cohere's Python client doesn't support async natively
        # For a real async implementation, you would need to use aiohttp directly
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate_embeddings, texts)
    
    def embed_document_chunks(self, chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """Generate embeddings for document chunks and return with metadata."""
        texts = [chunk.content for chunk in chunks]
        embeddings = self.generate_embeddings(texts)
        
        # Create a dictionary with embeddings and metadata
        embedded_chunks = {
            "ids": [f"chunk_{i}" for i in range(len(chunks))],
            "embeddings": embeddings,
            "metadatas": [chunk.metadata for chunk in chunks],
            "documents": texts
        }
        
        return embedded_chunks