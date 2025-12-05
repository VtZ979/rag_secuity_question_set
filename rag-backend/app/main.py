"""
FastAPI main application
"""
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.pipeline.rag_pipeline import initialize_rag, get_rag_response
from config.settings import ALLOWED_ORIGINS


# Request model
class QuestionRequest(BaseModel):
    """Request model for question endpoint."""
    question: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes RAG pipeline on startup.
    """
    print("Starting application...")
    initialize_rag()
    yield
    print("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="Augmented Security Knowledge Hub API",
    description="RAG-based API for answering software security questions",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if "*" not in ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """
    Root endpoint to verify server is running.
    
    Returns:
        Welcome message
    """
    return {
        "message": "Augmented Security Knowledge Hub API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy"}


@app.post("/askQuestion")
def ask_question(req: QuestionRequest):
    """
    Main endpoint for asking security-related questions.
    
    Args:
        req: QuestionRequest containing the user's question
        
    Returns:
        RAG response with answer and related posts
    """
    try:
        response = get_rag_response(req.question)
        return response
    except Exception as e:
        return {
            "error": str(e),
            "message": "An error occurred while processing your question."
        }

