import os
import tempfile
import logging
import shutil
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

# Configure logging
logger = logging.getLogger(__name__)

from .models import Document, QueryHistory
from .serializers import DocumentSerializer, QueryHistorySerializer, DocumentUploadSerializer, QuerySerializer

# Import local RAG system components
from .document_processor import DocumentProcessor
from .embedding import EmbeddingGenerator
from .vector_store import VectorStore
from .text_generation import TextGenerator
from .rag_config import config
from .system_info import SystemInfoView
from .query_history import QueryHistoryView


class DocumentListView(APIView):
    """API view for listing and uploading documents."""
    
    def get(self, request):
        """Get all documents."""
        documents = Document.objects.all().order_by('-upload_date')
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


class DocumentUploadView(APIView):
    """API view for uploading documents."""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        """Upload and process a document."""
        serializer = DocumentUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            # Get uploaded file
            uploaded_file = serializer.validated_data['file']
            title = serializer.validated_data['title']
            
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
                    
                    return Response(
                        DocumentSerializer(document).data,
                        status=status.HTTP_201_CREATED
                    )
                    
                except Exception as e:
                    # If processing fails, delete the saved file
                    if permanent_file_path.exists():
                        permanent_file_path.unlink()
                    return Response(
                        {"error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryView(APIView):
    """API view for querying the RAG system."""
    
    def post(self, request):
        """Process a query and return the response."""
        serializer = QuerySerializer(data=request.data)
        
        if serializer.is_valid():
            query_text = serializer.validated_data['query']
            
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
                
                return Response(response_data)
                
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryHistoryView(APIView):
    """API view for retrieving query history."""
    
    def get(self, request):
        """Get all query history."""
        queries = QueryHistory.objects.all().order_by('-timestamp')
        serializer = QueryHistorySerializer(queries, many=True)
        return Response(serializer.data)


class SystemInfoView(APIView):
    """API view for retrieving system information."""
    
    def get(self, request):
        """Get RAG system information."""
        try:
            vector_store = VectorStore()
            stats = vector_store.get_collection_stats()
            
            return Response({
                "document_count": stats["document_count"],
                "collection_name": stats["collection_name"],
                "persist_directory": stats["persist_directory"],
                "chunk_size": config.chunk_size,
                "chunk_overlap": config.chunk_overlap,
                "top_k_results": config.top_k_results
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )