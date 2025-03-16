"""Text generation module for the RAG system using Google's Gemini API."""

from typing import List, Dict, Any, Optional
import google.generativeai as genai
from tqdm import tqdm
from pathlib import Path

from .rag_config import config


class TextGenerator:
    """Generates text responses using Google's Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "models/gemini-2.0-pro-exp-02-05"):
        """Initialize the text generator with API key and model."""
        self.api_key = api_key or config.gemini_api_key
        self.model = model
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        # Initialize the model
        self.gemini_model = genai.GenerativeModel(
            model_name=self.model,
            generation_config=self.generation_config
        )
    
    def generate_response(self, query: str, context_docs: List[str]) -> str:
        """Generate a response based on the query and retrieved documents."""
        # Combine the context documents into a single context string
        context = "\n\n---\n\n".join(context_docs)
        
        # Create a prompt that includes the context and query
        prompt = f"""You are an AI assistant that answers questions based on the provided context.

Context information:
{context}

User question: {query}

Please answer the question based only on the provided context. If the context doesn't contain the information needed to answer the question, say "I don't have enough information to answer this question."

Important: Include citations to the source documents in your response. When you reference information from the context, mention the source document number (e.g., [Document 1], [Document 2, Page 3]).
"""
        
        # Generate the response
        response = self.gemini_model.generate_content(prompt)
        
        return response.text
    
    def format_search_results(self, search_results: Dict[str, Any]) -> List[str]:
        """Format search results from vector store for use in generation."""
        documents = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]
        distances = search_results.get("distances", [[]])[0]
        
        formatted_docs = []
        for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
            # Extract source information
            source = metadata.get("source", "Unknown")
            filename = metadata.get("filename", Path(source).name if isinstance(source, str) else "Unknown")
            page_num = metadata.get("page_num", None)
            chunk_index = metadata.get("chunk_index", "Unknown")
            position_percent = metadata.get("position_percent", None)
            excerpt = metadata.get("excerpt", None)
            
            # Build source citation
            source_citation = f"Source: {filename}"
            if page_num is not None:
                source_citation += f", Page {page_num}"
            if position_percent is not None:
                source_citation += f", Position {position_percent}%"
            if chunk_index != "Unknown":
                source_citation += f", Chunk {chunk_index}"
            
            # Format the document with enhanced source information
            formatted_doc = f"Document {i+1} ({source_citation}, Relevance: {1-distance:.2f})"
            if excerpt:
                formatted_doc += f"\nExcerpt: {excerpt}"
            formatted_doc += f"\n\n{doc}"
            
            formatted_docs.append(formatted_doc)
        
        return formatted_docs