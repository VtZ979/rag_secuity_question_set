# 🔧 Augmented Security Knowledge Hub - Backend

FastAPI backend for RAG-based security question answering system.

## 📋 Requirements

- Python **3.11.5** or higher
- pip
- Ollama with Llama3 model

## 🚀 Quick Start

### 1. Install Ollama and Llama3

```bash
# Install Ollama (visit https://ollama.com/download for your OS)
# Then pull the Llama3 model:
ollama pull llama3

# Test the model
ollama run llama3
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
# From the rag-backend directory
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## 📁 Project Structure

```
rag-backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── models/                 # ML models
│   │   ├── security_classifier.py
│   │   ├── lda_classifier.py
│   │   └── sentiment_analyzer.py
│   ├── services/               # Business logic services
│   │   ├── data_loader.py
│   │   ├── retriever_service.py
│   │   ├── llm_service.py
│   │   └── similarity_service.py
│   └── pipeline/
│       └── rag_pipeline.py     # Main RAG pipeline
├── config/
│   └── settings.py             # Configuration settings
├── data/                       # Data files (CSV, LDA models)
├── requirements.txt
└── README.md
```

## 🔌 API Endpoints

### GET `/`
Health check endpoint.

**Response:**
```json
{
  "message": "Augmented Security Knowledge Hub API",
  "status": "running",
  "version": "1.0.0"
}
```

### POST `/askQuestion`
Ask a security-related question.

**Request:**
```json
{
  "question": "How to prevent SQL injection in Java?"
}
```

**Response:**
```json
{
  "answer": {
    "user_question": "...",
    "llm_answer": "...",
    "challenges": "...",
    "skills": "...",
    "category": "..."
  },
  "related_post": [
    {
      "post_id": "...",
      "title": "...",
      "ori_question": "...",
      "accepted_answers": "...",
      "similarity": "...",
      "llmSolution": "...",
      "answer_similarity": "...",
      "challenges": "...",
      "skills": "...",
      "sentimental": "...",
      "category": "..."
    }
  ]
}
```

## ⚙️ Configuration

Edit `config/settings.py` to customize:

- Embedding model
- LLM model
- Retrieval settings
- API settings
- Data paths

## 🧪 Testing

```bash
# Test the API
curl http://localhost:8000/

# Ask a question
curl -X POST http://localhost:8000/askQuestion \
     -H "Content-Type: application/json" \
     -d '{"question": "How to prevent SQL injection?"}'
```

## 📝 Notes

- The first run will take time to load documents and build the vector database
- Ensure all data files are in the `data/` directory
- The SVM classifier model should be in `app/models/svm_classifier.joblib`

