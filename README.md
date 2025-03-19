# Ayandejo - A Modern RAG System

A Retrieval-Augmented Generation (RAG) system built with a Django backend and React frontend. The system uses Google's Gemini API for text generation and Cohere for embeddings.

## Features

- Document processing for PDF, TXT, and DOCX files
- Text chunking with configurable size and overlap
- Embeddings generation using Cohere's API
- Vector storage with ChromaDB
- Text generation using Google's Gemini API
- Interactive web interface with React
- RESTful API with Django
- Document management system
- Query history tracking

## Architecture

The project is structured as a full-stack application:

- **Backend**: Django REST framework providing API endpoints for document processing, vector storage, and text generation
- **Frontend**: React application with Material UI for a modern, responsive user interface

## Setup

### Prerequisites

- Python 3.9+
- Node.js 14+ and npm
- API keys for Google Gemini and Cohere

### Installation

1. Clone the repository or download the source code

2. Set up the backend:

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt
```

3. Set up the frontend:

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install
```

4. Configure your API keys in the `.env` file (copy from .env.example):

```
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here

# Vector DB Settings
CHROMA_PERSIST_DIRECTORY=./data/chroma

# RAG Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5

# Django Settings (optional)
DJANGO_SECRET_KEY=your_secret_key_here
DJANGO_DEBUG=True
```

## Usage

### Running the Application

1. Start the Django backend server:

```bash
# Navigate to the backend directory
cd backend

# Run migrations (first time only)
python manage.py migrate

# Start the development server
python manage.py runserver
```

2. Start the React frontend development server:

```bash
# Navigate to the frontend directory
cd frontend

# Start the development server
npm start
```

3. Access the web interface at http://localhost:3000

### Processing Documents

1. Upload documents through the web interface by navigating to the Documents page
2. The system will automatically process and index the documents

### Querying the RAG System

1. Navigate to the Query page in the web interface
2. Enter your question in the input field
3. View the generated response along with source references
4. Browse your query history in the History page

### Configuration

You can modify the following settings in the `.env` file:

```
# Vector DB Settings
CHROMA_PERSIST_DIRECTORY=./data/chroma

# RAG Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

## Project Structure

- `backend/`: Django backend
  - `rag_api/`: Main application code
    - `document_processor.py`: Document loading and chunking
    - `embedding.py`: Embedding generation with Cohere
    - `text_generation.py`: Text generation with Gemini
    - `vector_store.py`: Vector database management with ChromaDB
    - `views.py`: API endpoints
  - `rag_project/`: Django project settings
  - `manage.py`: Django management script
  - `requirements.txt`: Backend Python dependencies
- `frontend/`: React frontend
  - `src/`: Source code
    - `components/`: Reusable UI components
    - `pages/`: Application pages (Dashboard, Documents, Query, History)
    - `App.js`: Main application component
  - `package.json`: Frontend dependencies and scripts
- `documents/`: Directory for storing uploaded documents
- `data/`: Directory for storing processed data
- `.env`: Environment variables and configuration
- `requirements.txt`: Project-level Python dependencies

## License

MIT