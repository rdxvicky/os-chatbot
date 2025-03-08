# RAG API Documentation

A FastAPI-based Retrieval Augmented Generation (RAG) system that processes markdown documents and answers queries using OpenAI's language models.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Docker Deployment](#docker-deployment)
- [Usage Examples](#usage-examples)

## Overview

This API service implements a RAG system that:
- Loads and processes markdown documents
- Creates embeddings using OpenAI's embedding model
- Stores vectors in a FAISS database
- Answers queries using relevant document context

## Features

- Document Processing:
  - Recursive markdown file loading
  - Intelligent text chunking
  - Vector embeddings creation
- Query Processing:
  - Semantic similarity search
  - Context-aware responses
  - Source document tracking
- API Features:
  - RESTful endpoints
  - Health monitoring
  - Error handling
- Deployment:
  - Docker support
  - Environment configuration
  - Production-ready setup

## Prerequisites

- Python 3.11+
- OpenAI API key
- Docker (for containerized deployment)
- Directory of markdown documents

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Configuration

The system requires a directory of markdown files to process. Place your documents in the `ubuntu-docs` directory.

Key configuration parameters:
- Chunk size: 512 characters
- Chunk overlap: 100 characters
- Vector similarity search: top 3 results

## API Endpoints

### POST /query
Query the RAG system with a question.

**Request:**
```json
{
    "question": "What is Ubuntu Core?"
}
```

**Response:**
```json
{
    "answer": "Detailed answer based on the documents...",
    "sources": [
        "path/to/source1.md",
        "path/to/source2.md"
    ]
}
```

### GET /health
Check API health status.

**Response:**
```json
{
    "status": "healthy"
}
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t rag-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 --env-file .env rag-api
```

The API will be available at `http://localhost:8000`.

## Usage Examples

### Using curl:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Ubuntu Core?"}'
```

### Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"question": "What is Ubuntu Core?"}
)
print(response.json())
```

## Error Handling

The API returns standard HTTP status codes:
- 200: Successful query
- 500: Server error (e.g., QA system not initialized)
- Other errors include appropriate error messages in the response


