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
git clone [<repository-url>](https://github.com/rdxvicky/os-chatbot.git)
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
    "question": "How can i build an ubuntu Image?"
}
```

**Response:**
```json
{
    "answer": "To build an Ubuntu image, you can use the `ubuntu-image` tool. Here are the steps to do so:\n\n1. **Install `ubuntu-image`:** You need to install the `ubuntu-image` tool on a snap-supporting Linux system. You can do this by running the following command:\n\n   ```bash\n   sudo snap install ubuntu-image --beta --classic\n   ```\n\n2. **Prepare a Model Assertion:** The `ubuntu-image` command requires a model assertion file to build an image. Make sure you have this file ready.\n\n3. **Build the Image:** Once you have the model assertion file, you can build the image by running:\n\n   ```bash\n   ubuntu-image <model-assertion-file>\n   ```\n\nReplace `<model-assertion-file>` with the actual filename of your model assertion.\n\nNote: The `ubuntu-image` tool is currently in beta, and it will not auto-update. To get the latest version, you can periodically run:\n\n   ```bash\n   snap refresh --beta --devmode ubuntu-image\n   ```",
    "sources": [
        "ubuntu-docs/image/image-building.md",
    "ubuntu-docs/image/image-building.md",
    "ubuntu-docs/guides/build-device/board-enablement.md"
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
  -d '{"question": "How can i build an ubuntu Image?"}'
```

### Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"question": "How can i build an ubuntu Image?"}
)
print(response.json())
```

## Error Handling

The API returns standard HTTP status codes:
- 200: Successful query
- 500: Server error (e.g., QA system not initialized)
- Other errors include appropriate error messages in the response


