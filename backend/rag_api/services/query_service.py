import logging
from pathlib import Path

from ..models import Document, QueryHistory
from ..embedding import EmbeddingGenerator
from ..vector_store import VectorStore
from ..text_generation import TextGenerator

# Configure logging
logger = logging.getLogger(__name__)

class QueryService:
    """Service for handling query operations."""
    
    @staticmethod
    def get_query_history():
        """Get all query history ordered by timestamp."""
        return QueryHistory.objects.all().order_by('-timestamp')
    
    @staticmethod
    def process_query(query_text):
        """Process a query and return the response and source documents."""
        try:
            # Initialize RAG components
            embedding_generator = EmbeddingGenerator()
            vector_store = VectorStore()
            text_generator = TextGenerator()
            
            logger.info(f"Processing query: {query_text[:50]}...")
            
            # Generate query embedding
            query_embedding = embedding_generator.generate_query_embedding(query_text)
            logger.info("Generated query embedding")
            
            # Search for relevant documents
            search_results = vector_store.search(query_embedding)
            logger.info(f"Found {len(search_results.get('documents', [[]])[0])} relevant document chunks")
            
            # Format search results for better context
            formatted_docs = text_generator.format_search_results(search_results)
            
            # Generate response with formatted documents
            response_text = text_generator.generate_response(
                query_text, 
                formatted_docs
            )
            
            # Create query history record
            query_history = QueryHistory.objects.create(
                query_text=query_text,
                response_text=response_text
            )
            
            # Get document IDs from search results
            document_ids = set()
            for metadata in search_results.get("metadatas", [[]])[0]:
                source = metadata.get("source", "")
                filename = metadata.get("filename", "")
                
                # Try to find document by filename first
                if filename:
                    docs = Document.objects.filter(file_name__iexact=filename)
                    if docs.exists():
                        document_ids.add(docs.first().id)
                        continue
                
                # If no filename or no match, try with source path
                if source:
                    source_filename = Path(source).name
                    # Find document by filename - try both exact and case-insensitive match
                    docs = Document.objects.filter(file_name__iexact=source_filename)
                    if not docs.exists():
                        # Try with just the stem (filename without extension)
                        file_stem = Path(source_filename).stem
                        docs = Document.objects.filter(file_name__icontains=file_stem)
                    
                    if docs.exists():
                        document_ids.add(docs.first().id)
            
            # Add retrieved documents to query history
            if document_ids:
                query_history.documents_retrieved.add(*document_ids)
            
            # Format response
            response_data = {
                "query": query_text,
                "response": response_text,
                "sources": [
                    {
                        "content": doc[:200] + "..." if len(doc) > 200 else doc,
                        "metadata": metadata
                    }
                    for doc, metadata in zip(
                        search_results.get("documents", [[]])[0],
                        search_results.get("metadatas", [[]])[0]
                    )
                ]
            }
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise 