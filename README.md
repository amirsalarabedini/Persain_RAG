# Ayandejo RAG System

A Retrieval-Augmented Generation (RAG) system built with Google's Gemini API for text generation and Cohere for embeddings.

## Features

- Document processing for PDF, TXT, and DOCX files
- Text chunking with configurable size and overlap
- Embeddings generation using Cohere's API
- Vector storage with ChromaDB
- Text generation using Google's Gemini API
- Interactive query mode

## Setup

### Prerequisites

- Python 3.9+
- API keys for Google Gemini and Cohere

### Installation

1. Clone the repository or download the source code

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Configure your API keys in the `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
```

## Usage

### Processing Documents

Place your documents (PDF, TXT, DOCX) in the `documents` directory.

### Running the RAG System

To set up the system and process documents:

```bash
python main.py --setup-only
```

To ask a single question:

```bash
python main.py --query "What is the main topic of these documents?"
```

To run in interactive mode:

```bash
python main.py --interactive
```

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

- `src/`: Source code directory
  - `config.py`: Configuration management
  - `document_processor.py`: Document loading and chunking
  - `embedding.py`: Embedding generation with Cohere
  - `text_generation.py`: Text generation with Gemini
  - `vector_store.py`: Vector database management with ChromaDB
- `main.py`: Main entry point
- `requirements.txt`: Required Python packages
- `.env`: Environment variables and configuration
- `documents/`: Directory for storing documents to process
- `data/`: Directory for storing processed data

## License

MIT