# Set offline mode and warnings BEFORE importing any HuggingFace/sentence-transformers modules
import os
import warnings
import logging

# Set offline mode to disable network checks (model should already be cached locally)
# Set these BEFORE any imports that might use HuggingFace
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_OFFLINE_WARNING'] = '1'
os.environ['HF_HUB_DISABLE_EXPERIMENTAL_WARNING'] = '1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'

# Ignore warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Set logging levels to ERROR to suppress network timeout messages
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .pipeline.rag_pipeline import initialize_rag, get_rag_response
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import traceback


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing RAG pipeline...")
    initialize_rag()
    yield
    print("Shutting down...")
    

app = FastAPI(lifespan=lifespan)

# Define allowed origins for CORS (Cross-Origin Resource Sharing)
# Get allowed origins from environment variable or use defaults
import os

# Get VPS IP from environment or detect automatically
VPS_IP = os.getenv("VPS_IP", "")
if not VPS_IP:
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        VPS_IP = s.getsockname()[0]
        s.close()
    except:
        VPS_IP = ""

# Build allowed origins list
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
if VPS_IP:
    origins.extend([
        f"http://{VPS_IP}:5173",
        f"http://{VPS_IP}:8001",
    ])

# Also allow from environment variable
ALLOWED_ORIGINS_ENV = os.getenv("ALLOWED_ORIGINS", "")
if ALLOWED_ORIGINS_ENV:
    origins.extend(ALLOWED_ORIGINS_ENV.split(","))

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic GET endpoint to verify server is running
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# Define the input schema for /askQuestion POST requests
class EchoRequest(BaseModel):
    question: str

# Endpoint to receive a question and return the RAG response
@app.post("/askQuestion")
def echo(req: EchoRequest):
    try:
        if not req.question or not req.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        response = get_rag_response(req.question)
        return response
    except HTTPException:
        # Re-raise HTTP exceptions (like 400) to preserve status code
        raise
    except Exception as e:
        # Log the full error for debugging
        print(f"Error processing question: {e}")
        print(traceback.format_exc())
        # Return a proper error response with CORS headers
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": "An error occurred while processing your question. Please try again later.",
                "details": str(e) if str(e) else "Unknown error"
            }
        )