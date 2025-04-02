import os
import logging
import tempfile
import shutil
from pathlib import Path

from django.conf import settings
from ..models import Document
from ..document_processor import DocumentProcessor
from ..embedding import EmbeddingGenerator
from ..vector_store import VectorStore
from ..rag_config import config

# Configure logging
logger = logging.getLogger(__name__)

class DocumentService:
    """Service for handling document operations."""
    
    @staticmethod
    def get_all_documents():
        """Get all documents ordered by upload date."""
        return Document.objects.all().order_by('-upload_date')
    
    @staticmethod
    def process_and_save_document(uploaded_file, title):
        """Process and save a document, returning the created document record."""
        # Create documents directory if it doesn't exist
        documents_dir = Path(config.documents_directory)
        documents_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file to documents directory
        permanent_file_path = documents_dir / uploaded_file.name
        with open(permanent_file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / uploaded_file.name
            
            # Copy file to temporary directory for processing
            shutil.copy2(permanent_file_path, file_path)
            
            try:
                # Initialize RAG components
                doc_processor = DocumentProcessor()
                embedding_generator = EmbeddingGenerator()
                vector_store = VectorStore()
                
                logger.info(f"Processing document: {uploaded_file.name} in {temp_dir}")
                
                # Process document
                documents = doc_processor.load_documents(temp_dir)
                logger.info(f"Loaded {len(documents)} document(s) from {uploaded_file.name}")
                
                chunks = doc_processor.process_documents(documents)
                logger.info(f"Created {len(chunks)} chunks from {uploaded_file.name}")
                
                # Log chunk metadata for debugging
                for i, chunk in enumerate(chunks[:2]):  # Log first two chunks for debugging
                    logger.debug(f"Chunk {i} metadata: {chunk.metadata}")
                
                embedded_chunks = embedding_generator.embed_document_chunks(chunks)
                logger.info(f"Generated embeddings for {len(embedded_chunks['ids'])} chunks")
                
                vector_store.add_documents(embedded_chunks)
                logger.info(f"Added document chunks to vector store")
                
                # Save document record
                document = Document.objects.create(
                    title=title,
                    file_name=uploaded_file.name,
                    file_type=uploaded_file.name.split('.')[-1],
                    chunk_count=len(chunks)
                )
                logger.info(f"Created document record in database: {document.id} - {document.title}")
                
                return document
                
            except Exception as e:
                # If processing fails, delete the saved file
                if permanent_file_path.exists():
                    permanent_file_path.unlink()
                logger.error(f"Error processing document: {str(e)}")
                raise 