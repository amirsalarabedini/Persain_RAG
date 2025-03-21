"""Document processing module for the RAG system."""

import os
from pathlib import Path
from typing import List, Dict, Union, Optional
import PyPDF2
import docx2txt
from tqdm import tqdm

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
    """Processes documents for the RAG system."""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """Initialize the document processor with chunking parameters."""
        self.chunk_size = chunk_size or config.chunk_size
        self.chunk_overlap = chunk_overlap or config.chunk_overlap
    
    def load_document(self, file_path: Union[str, Path]) -> Union[Document, List[Document]]:
        """Load a document from a file path.
        
        For PDF files, returns a list of Documents (one per page).
        For other file types, returns a single Document.
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = file_path.suffix.lower()
        
        if file_extension == ".pdf":
            # For PDFs, load with page tracking
            return self._load_pdf_with_pages(file_path)
        
        # For non-PDF files, create a single document
        metadata = {
            "source": str(file_path),
            "filename": file_path.name,
            "file_type": file_extension[1:] if file_extension else "unknown"
        }
        
        if file_extension == ".txt":
            content = self._load_text(file_path)
        elif file_extension in [".docx", ".doc"]:
            content = self._load_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        return Document(content=content, metadata=metadata)
    
    def load_documents(self, directory: Union[str, Path]) -> List[Document]:
        """Load all supported documents from a directory."""
        directory = Path(directory)
        if not directory.exists() or not directory.is_dir():
            raise NotADirectoryError(f"Directory not found: {directory}")
        
        documents = []
        supported_extensions = [".pdf", ".txt", ".docx", ".doc"]
        
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
    
    def _load_pdf(self, file_path: Path) -> str:
        """Load content from a PDF file."""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
            
    def _load_pdf_with_pages(self, file_path: Path) -> List[Document]:
        """Load content from a PDF file with page tracking."""
        documents = []
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(reader.pages):
                content = page.extract_text()
                if content.strip():  # Skip empty pages
                    metadata = {
                        "source": str(file_path),
                        "filename": file_path.name,
                        "file_type": "pdf",
                        "page_num": i + 1,
                        "total_pages": len(reader.pages)
                    }
                    documents.append(Document(content=content, metadata=metadata))
        return documents
    
    def _load_text(self, file_path: Path) -> str:
        """Load content from a text file."""
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            return file.read()
    
    def _load_docx(self, file_path: Path) -> str:
        """Load content from a DOCX file."""
        return docx2txt.process(str(file_path))