# Persian RAG Backend

This is the backend component of the Persian RAG system. It provides a RESTful API for document management, vector search, and query processing.

## Project Structure

The project follows a clean, modular architecture for better maintainability and scalability:

```
backend/
├── data/                # Data storage (documents, vector store)
├── rag_api/             # Main API application
│   ├── migrations/      # Database migrations
│   ├── models/          # Database models
│   │   ├── document.py
│   │   └── query_history.py
│   ├── serializers/     # API serializers
│   │   ├── document_serializers.py
│   │   └── query_serializers.py
│   ├── services/        # Business logic services
│   │   ├── document_service.py
│   │   ├── query_service.py
│   │   └── system_service.py
│   ├── urls/            # URL routing
│   │   └── api_urls.py
│   ├── utils/           # Utilities and helpers
│   │   └── error_handlers.py
│   ├── views/           # API views and controllers
│   │   ├── document_views.py
│   │   ├── query_views.py
│   │   └── system_views.py
│   ├── admin.py         # Django admin configuration
│   ├── document_processor.py  # Document processing logic
│   ├── embedding.py     # Embedding generation with Cohere
│   ├── models.py        # Main models definition
│   ├── query_history.py # Query history tracking
│   ├── rag_config.py    # RAG system configuration
│   ├── serializers.py   # Main serializers
│   ├── system_info.py   # System information utilities
│   ├── text_generation.py  # Text generation with Gemini
│   ├── urls.py          # API URL routing
│   ├── vector_store.py  # Vector store operations with ChromaDB
│   ├── views.py         # Main API views
│   └── views_sources.py # Source document views
├── rag_project/         # Django project settings
│   ├── settings.py      # Project settings
│   └── urls.py          # Main URL routing
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## Key Components

1. **Document Processor**: Handles loading, parsing, and chunking of PDF, TXT, and DOCX files
2. **Embedding Engine**: Generates embeddings using Cohere's API
3. **Vector Store**: Manages document vectors with ChromaDB
4. **Text Generation**: Interfaces with Google's Gemini API for response generation
5. **API Layer**: RESTful endpoints for document management and query processing

## API Endpoints

- `GET /api/documents/`: List all documents
- `POST /api/documents/upload/`: Upload a new document
- `DELETE /api/documents/{id}/`: Delete a document
- `POST /api/query/`: Process a query against the document collection
- `GET /api/query/history/`: Get query history
- `GET /api/system/info/`: Get system information

## Setup and Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   Create a `.env` file with the following variables:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   CHROMA_PERSIST_DIRECTORY=./data/chroma
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   TOP_K_RESULTS=5
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

## Technologies Used

- **Django & Django REST Framework**: Web framework and API development
- **ChromaDB**: Vector database for storing and retrieving document embeddings
- **Cohere**: API for generating text embeddings
- **Google Gemini**: Large language model for text generation
- **Docling**: Document processing and chunking