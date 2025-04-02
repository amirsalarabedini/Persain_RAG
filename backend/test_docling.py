#!/usr/bin/env python
"""Test script for Docling integration with the backend."""

import os
import sys
from pathlib import Path

# Add the current directory to the path so we can import from rag_api
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_api.document_processor import DocumentProcessor

def test_docling_integration():
    """Test basic Docling functionality with a sample document."""
    # Initialize document processor
    processor = DocumentProcessor()
    print("Document processor initialized with Docling")
    
    # Test with a sample document if provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            print(f"Processing document: {file_path}")
            try:
                result = processor.load_document(file_path)
                if isinstance(result, list):
                    print(f"Successfully processed document into {len(result)} pages")
                    for i, doc in enumerate(result[:2]):  # Show first 2 pages only
                        print(f"\nPage {i+1} preview:")
                        print(doc.content[:200] + "..." if len(doc.content) > 200 else doc.content)
                        print(f"Metadata: {doc.metadata}")
                else:
                    print("Successfully processed document")
                    print("\nDocument preview:")
                    print(result.content[:200] + "..." if len(result.content) > 200 else result.content)
                    print(f"Metadata: {result.metadata}")
                
                # Test chunking
                if isinstance(result, list):
                    chunks = processor.chunk_document(result[0])  # Chunk first page only
                else:
                    chunks = processor.chunk_document(result)
                
                print(f"\nChunking created {len(chunks)} chunks")
                if chunks:
                    print("First chunk preview:")
                    print(chunks[0].content[:100] + "..." if len(chunks[0].content) > 100 else chunks[0].content)
                    print(f"Chunk metadata: {chunks[0].metadata}")
                
                return True
            except Exception as e:
                print(f"Error processing document: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print(f"File not found: {file_path}")
            return False
    else:
        print("No document provided. Usage: python test_docling.py <path/to/document>")
        return True  # Basic initialization test passed

if __name__ == "__main__":
    success = test_docling_integration()
    sys.exit(0 if success else 1) 