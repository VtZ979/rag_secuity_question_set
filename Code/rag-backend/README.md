# 🔧 FastAPI RAG Project

This project is a FastAPI backend integrating a Retrieval-Augmented Generation (RAG) pipeline to answer software security-related questions using LLMs.

## ⚙️ Requirements

- Python **3.11.5**
- pip

---

## 🤖 Step 1: Install and Run Ollama + Llama3

### 📌 What is Ollama?

> [Ollama](https://ollama.com) lets you run LLMs (like Llama3, Mistral, etc.) **locally on your machine**, with GPU or CPU support. It's lightweight, easy to use, and ideal for local LLM development.

---

### 🧩 1. Install Ollama

#### ✅ For macOS:

```bash
brew install ollama
```

Or visit the official website to download the installer:  
👉 https://ollama.com/download

#### ✅ For Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

> ⚠️ Windows users need to use WSL (Windows Subsystem for Linux).

---

### 🧠 2. Pull the Llama3 model

```bash
ollama pull llama3
```

This will download the latest Llama 3 model from the official Ollama model library.

---

### 🚀 3. Run and test the model

```bash
ollama run llama3
```

If everything works correctly, you will see the model start and be able to interact with it.

---

> 💡 Tip: You don't need to manually run the model every time — the RAG application can automatically call the Ollama backend service.

---

## 🚀 Step 2: Set Up Environment and Run the Server

### ⬇️ Install dependencies and start FastAPI

```bash
# Install all required packages
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

## 📬 Step 3: Test the API

### ✅ 1. Check if the server is running

Use the root `GET /` endpoint to verify the server is live:

```bash
curl http://127.0.0.1:8000/

{
  "message": "Hello, FastAPI!"
}
```

### ✅ 2. Ask a question

Ask a question using the RAG API
Use the `POST /askQuestion` endpoint to send your question:

```bash
curl -X POST http://127.0.0.1:8000/askQuestion \
     -H "Content-Type: application/json" \
     -d '{"question": "How to prevent SQL injection in a Java web app?"}'

```

Example response:

```bash
[
  {
    "post_id": "43865975",
    "title": "mime type strict error in Spring",
    "question": "...",
    "ori_question": "...",
    "answers": "...",
    "accepted answers": "...",
    "similarity": 0.91,
    "llm_response": "To prevent SQL injection in Java...",
    "challenges": "...",
    "skills": "Spring Security, SQL handling"
  },
  ...
]

```
