from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import List, Dict

# Import functions from test.py
from test import (
    load_markdown_files,
    process_documents,
    create_vector_store,
    initialize_qa_system
)

app = FastAPI(title="RAG API", description="API for RAG-based Q&A system")

# Initialize the QA system at startup
qa_system = None

class Query(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
    sources: List[str]

@app.on_event("startup")
async def startup_event():
    """Initialize the QA system when the API starts"""
    global qa_system
    
    # Set up OpenAI API key
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    
    # Load and process documents
    directory_path = 'ubuntu-docs'
    documents = load_markdown_files(directory_path)
    processed_docs = process_documents(documents)
    
    # Create vector store and initialize QA system
    vector_store = create_vector_store(processed_docs)
    qa_system = initialize_qa_system(vector_store)

@app.post("/query", response_model=Answer)
async def query_documents(query: Query) -> Dict:
    """
    Process a query and return the answer with source documents
    
    Args:
        query (Query): The query object containing the question
        
    Returns:
        Dict: Contains the answer and list of source documents
    """
    if not qa_system:
        raise HTTPException(status_code=500, detail="QA system not initialized")
    
    try:
        result = qa_system.invoke({"query": query.question})
        return {
            "answer": result['result'],
            "sources": [doc.metadata['source'] for doc in result['source_documents']]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}
