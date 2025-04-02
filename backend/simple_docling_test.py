#!/usr/bin/env python
"""Simple standalone test script for Docling."""

import os
import sys
from pathlib import Path
from docling.document_converter import DocumentConverter

def test_docling():
    """Test basic Docling functionality with a sample document."""
    if len(sys.argv) < 2:
        print("Usage: python simple_docling_test.py <path/to/document>")
        return False
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    print(f"Processing document: {file_path}")
    try:
        # Initialize Docling converter
        converter = DocumentConverter()
        print("DocumentConverter initialized")
        
        # Convert the document
        result = converter.convert(file_path)
        print("Document converted successfully")
        
        # Show document info
        print(f"\nDocument info:")
        print(f"Title: {getattr(result.document, 'title', 'N/A')}")
        
        # Check if pages attribute exists and show count
        if hasattr(result.document, 'pages'):
            pages = result.document.pages
            if isinstance(pages, dict):
                num_pages = len(pages.keys())
                print(f"Number of pages: {num_pages} (dictionary)")
                # Get the first page key
                first_page_key = list(pages.keys())[0] if pages else None
            elif isinstance(pages, list):
                num_pages = len(pages)
                print(f"Number of pages: {num_pages} (list)")
                first_page_key = 0 if pages else None
            else:
                print(f"Pages is of type: {type(pages)}")
                first_page_key = None
        else:
            print("Document has no pages attribute")
            first_page_key = None
        
        # Export document to markdown
        markdown = result.document.export_to_markdown()
        print(f"\nMarkdown preview (first 300 chars):")
        print(markdown[:300] + "..." if len(markdown) > 300 else markdown)
        
        # If it's a PDF, show first page content
        if first_page_key is not None:
            try:
                first_page = result.document.pages[first_page_key]
                page_markdown = first_page.export_to_markdown()
                print(f"\nFirst page preview (first 300 chars):")
                print(page_markdown[:300] + "..." if len(page_markdown) > 300 else page_markdown)
            except Exception as e:
                print(f"Error accessing first page: {e}")
                print(f"Page keys: {list(result.document.pages.keys()) if isinstance(result.document.pages, dict) else 'N/A'}")
        
        # Show document structure
        print("\nDocument attributes:")
        for attr in dir(result.document):
            if not attr.startswith('_') and not callable(getattr(result.document, attr)):
                print(f"- {attr}")
        
        return True
    except Exception as e:
        print(f"Error processing document: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_docling()
    sys.exit(0 if success else 1) 