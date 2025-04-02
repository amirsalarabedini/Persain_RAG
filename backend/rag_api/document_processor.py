"""Document processing module for the RAG system using Docling."""

import os
from pathlib import Path
from typing import List, Dict, Union, Optional
from tqdm import tqdm

# Import Docling components
from docling.document_converter import DocumentConverter

from .rag_config import config


class Document:
    """Represents a document with content and metadata."""
    
    def __init__(self, content: str, metadata: Optional[Dict] = None):
        """Initialize a document with content and optional metadata."""
        self.content = content
        self.metadata = metadata or {}
    
    def __repr__(self) -> str:
        """String representation of the document."""
        return f"Document(metadata={self.metadata}, content_preview={self.content[:50]}...)"


class DocumentChunk:
    """Represents a chunk of a document with content and metadata."""
    
    def __init__(self, content: str, metadata: Optional[Dict] = None):
        """Initialize a document chunk with content and optional metadata."""
        self.content = content
        self.metadata = metadata or {}
    
    def __repr__(self) -> str:
        """String representation of the document chunk."""
        return f"DocumentChunk(metadata={self.metadata}, content_preview={self.content[:50]}...)"


class DocumentProcessor:
    """Processes documents for the RAG system using Docling."""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """Initialize the document processor with chunking parameters."""
        self.chunk_size = chunk_size or config.chunk_size
        self.chunk_overlap = chunk_overlap or config.chunk_overlap
        
        # Initialize Docling converter
        self.converter = DocumentConverter()
    
    def load_document(self, file_path: Union[str, Path]) -> Union[Document, List[Document]]:
        """Load a document from a file path using Docling.
        
        For PDF files, returns a list of Documents (one per page).
        For other file types, returns a single Document.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = file_path.suffix.lower()
        
        # Base metadata for all document types
        base_metadata = {
            "source": str(file_path),
            "filename": file_path.name,
            "file_type": file_extension[1:] if file_extension else "unknown"
        }
        
        # Use Docling to process the document
        try:
            # Convert the document using Docling
            result = self.converter.convert(str(file_path))
            
            # Get the full document content
            full_content = result.document.export_to_markdown()
            
            if file_extension == ".pdf" and hasattr(result.document, 'pages'):
                # For PDFs, create one document per page to maintain compatibility
                documents = []
                pages = result.document.pages
                
                # Docling pages can be a dictionary with page numbers as keys
                if isinstance(pages, dict):
                    page_keys = sorted(pages.keys())
                    total_pages = len(page_keys)
                    
                    # If the PDF has only one page or no page content, just use the full document
                    if total_pages == 0 or (total_pages == 1 and not pages[page_keys[0]]):
                        return Document(content=full_content, metadata=base_metadata)
                    
                    # Try to split the content by page markers
                    import re
                    page_markers = re.findall(r'# Page \d+', full_content)
                    page_content_split = None
                    
                    if len(page_markers) >= len(page_keys):
                        page_content_split = re.split(r'(?=# Page \d+)', full_content)
                        # Remove the first element if it's empty (content before first page marker)
                        if page_content_split and not page_content_split[0].strip():
                            page_content_split = page_content_split[1:]
                    
                    for i, page_num in enumerate(page_keys):
                        page = pages[page_num]
                        
                        # Try to get content from the page split if available
                        if page_content_split and i < len(page_content_split):
                            page_content = page_content_split[i]
                        else:
                            # Try to get content from the page object
                            try:
                                if hasattr(page, 'export_to_markdown'):
                                    page_content = page.export_to_markdown()
                                else:
                                    # Create markdown from page elements
                                    page_content = self._extract_page_content(page)
                            except Exception as e:
                                print(f"Error extracting page {page_num} content: {e}")
                                # Use a placeholder for this page
                                page_content = f"# Page {page_num}\n\n[Content extraction error]"
                        
                        # Create metadata for the page
                        page_metadata = base_metadata.copy()
                        page_metadata.update({
                            "page_num": page_num,
                            "total_pages": total_pages
                        })
                        
                        documents.append(Document(content=page_content, metadata=page_metadata))
                    
                    return documents
                else:
                    # Create a single document from the entire PDF
                    return Document(content=full_content, metadata=base_metadata)
            else:
                # For non-PDF files or when page information isn't available
                return Document(content=full_content, metadata=base_metadata)
                
        except Exception as e:
            # Fallback to basic processing if Docling fails
            print(f"Docling processing failed for {file_path}: {e}. Using basic fallback processing.")
            return self._fallback_load_document(file_path, base_metadata)
    
    def _extract_page_content(self, page) -> str:
        """Extract content from a Docling page when export_to_markdown is not available."""
        content = []
        
        # Try to get the full document content as markdown
        if hasattr(page, 'export_to_text'):
            return page.export_to_text()
            
        # Get the document structure
        if hasattr(page, 'body'):
            # Just convert the entire document to markdown
            result = self.converter.result
            if result and hasattr(result, 'document'):
                return result.document.export_to_markdown()
        
        # Extract text from the page
        if hasattr(page, 'texts') and page.texts:
            for text in page.texts:
                if hasattr(text, 'text') and text.text:
                    content.append(text.text)
        
        # Extract tables if present
        if hasattr(page, 'tables') and page.tables:
            for table in page.tables:
                content.append("TABLE:")
                if hasattr(table, 'cells') and table.cells:
                    for cell in table.cells:
                        if hasattr(cell, 'text') and cell.text:
                            content.append(f"  - {cell.text}")
        
        # If still no content, try exporting raw page data
        if not content and hasattr(page, 'dict'):
            import json
            try:
                # Convert page data to JSON and back to extract text content
                page_data = page.dict()
                return f"Page data: {json.dumps(page_data, indent=2)}"
            except Exception as e:
                print(f"Error converting page data to JSON: {e}")
        
        # If still no content, use fallback with raw page attributes
        if not content:
            for attr in dir(page):
                if not attr.startswith('_') and not callable(getattr(page, attr)):
                    attr_value = getattr(page, attr)
                    if isinstance(attr_value, str) and attr_value.strip():
                        content.append(f"{attr}: {attr_value}")
        
        # If still no content, get full document markdown
        if not content:
            try:
                doc = getattr(self.converter, 'result', None)
                if doc and hasattr(doc, 'document'):
                    doc_content = doc.document.export_to_markdown()
                    # Split content by pages
                    import re
                    pages = re.split(r'(?=# Page \d+)', doc_content)
                    if len(pages) > 1:
                        return pages[1]  # First page content
                    return doc_content
            except Exception as e:
                print(f"Error getting document content: {e}")
        
        return "\n".join(content) if content else "No content extracted from page"
    
    def load_documents(self, directory: Union[str, Path]) -> List[Document]:
        """Load all supported documents from a directory."""
        directory = Path(directory)
        if not directory.exists() or not directory.is_dir():
            raise NotADirectoryError(f"Directory not found: {directory}")
        
        documents = []
        supported_extensions = [".pdf", ".txt", ".docx", ".doc", ".xlsx", ".pptx", ".html"]
        
        for file_path in tqdm(list(directory.glob("**/*")), desc="Loading documents"):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    result = self.load_document(file_path)
                    # Handle both single documents and lists of documents (from PDFs)
                    if isinstance(result, list):
                        documents.extend(result)
                    else:
                        documents.append(result)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        
        return documents
    
    def chunk_document(self, document: Document) -> List[DocumentChunk]:
        """Split a document into chunks with overlap."""
        content = document.content
        chunks = []
        
        # Simple text chunking by characters with overlap
        for i in range(0, len(content), self.chunk_size - self.chunk_overlap):
            chunk_content = content[i:i + self.chunk_size]
            if not chunk_content.strip():  # Skip empty chunks
                continue
                
            # Create metadata for the chunk
            chunk_metadata = document.metadata.copy()
            chunk_metadata["chunk_index"] = len(chunks)
            chunk_metadata["chunk_start_char"] = i
            chunk_metadata["chunk_end_char"] = i + len(chunk_content)
            
            # Add excerpt for context
            excerpt = chunk_content[:100] + "..." if len(chunk_content) > 100 else chunk_content
            chunk_metadata["excerpt"] = excerpt.replace("\n", " ").strip()
            
            # Add position information for better source tracking
            total_chars = len(content)
            if total_chars > 0:
                position_percent = (i / total_chars) * 100
                chunk_metadata["position_percent"] = round(position_percent, 2)
            
            chunks.append(DocumentChunk(content=chunk_content, metadata=chunk_metadata))
        
        return chunks
    
    def process_documents(self, documents: List[Document]) -> List[DocumentChunk]:
        """Process a list of documents into chunks."""
        all_chunks = []
        for document in tqdm(documents, desc="Chunking documents"):
            chunks = self.chunk_document(document)
            all_chunks.extend(chunks)
        return all_chunks
    
    def _fallback_load_document(self, file_path: Path, base_metadata: Dict) -> Union[Document, List[Document]]:
        """Fallback method to load documents when Docling fails."""
        file_extension = file_path.suffix.lower()
        
        if file_extension == ".pdf":
            try:
                import PyPDF2
                documents = []
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    for i, page in enumerate(reader.pages):
                        content = page.extract_text()
                        if content.strip():  # Skip empty pages
                            metadata = base_metadata.copy()
                            metadata.update({
                                "page_num": i + 1,
                                "total_pages": len(reader.pages)
                            })
                            documents.append(Document(content=content, metadata=metadata))
                return documents
            except Exception as e:
                print(f"Fallback PDF processing failed: {e}")
                raise
                
        elif file_extension == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="replace") as file:
                content = file.read()
                return Document(content=content, metadata=base_metadata)
                
        elif file_extension in [".docx", ".doc"]:
            try:
                import docx2txt
                content = docx2txt.process(str(file_path))
                return Document(content=content, metadata=base_metadata)
            except Exception as e:
                print(f"Fallback DOCX processing failed: {e}")
                raise
                
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")