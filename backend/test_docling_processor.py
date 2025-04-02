#!/usr/bin/env python
"""Test script for document processor with Docling integration."""

import os
import sys
from pathlib import Path

# Add the current directory to the path so we can import from rag_api
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# This allows importing without Django settings for testing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rag_project.settings")

# Setup RAG settings for testing
import django
from django.conf import settings

# Configure settings if they're not already configured
if not settings.configured:
    settings.configure(
        RAG_SETTINGS={
            'CHROMA_PERSIST_DIRECTORY': 'data/chroma',
            'DOCUMENTS_DIRECTORY': '../documents',
            'CHUNK_SIZE': 1000,
            'CHUNK_OVERLAP': 200,
            'TOP_K_RESULTS': 5,
        }
    )
    django.setup()

from rag_api.document_processor import DocumentProcessor

def test_docling_processor():
    """Test the document processor with Docling integration."""
    if len(sys.argv) < 2:
        print("Usage: python test_docling_processor.py <path/to/document>")
        return False
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    print(f"Processing document: {file_path}")
    try:
        # Initialize document processor
        processor = DocumentProcessor()
        print("Document processor initialized with Docling")
        
        # Process document
        result = processor.load_document(file_path)
        
        if isinstance(result, list):
            print(f"Successfully processed document into {len(result)} pages")
            for i, doc in enumerate(result[:2]):  # Show first 2 pages only
                print(f"\nPage {i+1} preview:")
                print(doc.content[:200] + "..." if len(doc.content) > 200 else doc.content)
                print(f"Metadata: {doc.metadata}")
                
                # Test chunking on first page
                if i == 0:
                    chunks = processor.chunk_document(doc)
                    print(f"\nChunking first page created {len(chunks)} chunks")
                    if chunks:
                        print("First chunk preview:")
                        print(chunks[0].content[:100] + "..." if len(chunks[0].content) > 100 else chunks[0].content)
        else:
            print("Successfully processed document")
            print("\nDocument preview:")
            print(result.content[:200] + "..." if len(result.content) > 200 else result.content)
            print(f"Metadata: {result.metadata}")
            
            # Test chunking
            chunks = processor.chunk_document(result)
            print(f"\nChunking created {len(chunks)} chunks")
            if chunks:
                print("First chunk preview:")
                print(chunks[0].content[:100] + "..." if len(chunks[0].content) > 100 else chunks[0].content)
        
        return True
    except Exception as e:
        print(f"Error processing document: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_docling_processor()
    sys.exit(0 if success else 1) 