"""
Application configuration settings
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data paths
DATA_DIR = BASE_DIR / "data"
CSV_DATA_PATH = DATA_DIR / "StackOverflow_security_sample_labelled_all.csv"
LDA_DIR = DATA_DIR / "LDA_doc"
LDA_MODEL_PATH = LDA_DIR / "lda_model_best_7topics.model"
LDA_DICT_PATH = LDA_DIR / "lda_dictionary.dict"
LDA_MAPPING_PATH = LDA_DIR / "topic_category_mapping.json"
CLASSIFIER_MODEL_PATH = BASE_DIR / "app" / "models" / "svm_classifier.joblib"

# Vector database settings
VECTOR_DB_DIR = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# LLM settings
LLM_MODEL = "llama3"
LLM_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Retrieval settings
RETRIEVAL_SEARCH_TYPE = "mmr"  # Options: "similarity", "mmr", "similarity_score_threshold"
RETRIEVAL_K = 3  # Number of documents to retrieve

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]

