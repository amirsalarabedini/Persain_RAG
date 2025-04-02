# Persian RAG Backend

This is the backend component of the Persian RAG system. It provides a RESTful API for document management, vector search, and query processing.

## Project Structure

The project follows a clean, modular architecture for better maintainability and scalability:

```
backend/
├── data/                # Data storage (documents, vector store)
├── rag_api/             # Main API application
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
│   ├── document_processor.py    # Document processing logic
│   ├── embedding.py            # Embedding generation
│   ├── vector_store.py         # Vector store operations
│   └── text_generation.py      # Text generation with LLMs
├── rag_project/         # Django project settings
│   ├── settings.py      # Project settings
│   └── urls.py          # Main URL routing
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## Key Components

1. **Models**: Database models for storing document metadata and query history
2. **Serializers**: Handle API request/response formatting
3. **Services**: Contain core business logic, separated from views
4. **Views**: Handle HTTP requests and responses
5. **Utils**: Common utilities including error handling

## API Endpoints

- `GET /api/documents/`: List all documents
- `POST /api/documents/upload/`: Upload a new document
- `POST /api/query/`: Process a query against the document collection
- `GET /api/query/history/`: Get query history
- `GET /api/system/info/`: Get system information

## Setup and Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py migrate
   ```

3. Start the development server:
   ```
   python manage.py runserver
   ``` 