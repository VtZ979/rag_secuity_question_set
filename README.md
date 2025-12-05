# Augmented Security Knowledge Hub - Final Version

This is the refactored and cleaned-up version of the RAG-based security knowledge hub project. The code has been reorganized for better maintainability, clarity, and demonstration purposes.

## 📁 Project Structure

```
final version/
├── rag-backend/          # FastAPI backend
│   ├── app/
│   │   ├── main.py       # FastAPI application
│   │   ├── models/       # ML models (classifiers, analyzers)
│   │   ├── services/     # Business logic services
│   │   └── pipeline/     # RAG pipeline
│   ├── config/           # Configuration
│   ├── data/             # Data files (CSV, models)
│   ├── requirements.txt
│   └── README.md
│
└── rag-frontend/         # React frontend
    ├── src/
    │   ├── components/   # React components
    │   ├── config/       # Configuration
    │   ├── services/     # API services
    │   └── App.jsx       # Main app
    ├── package.json
    └── README.md
```

## 🚀 Quick Start

### Backend Setup

1. Install Ollama and pull Llama3:
```bash
ollama pull llama3
```

2. Install Python dependencies:
```bash
cd rag-backend
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. Install dependencies:
```bash
cd rag-frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

## ✨ Improvements Made

### Backend Improvements

1. **Modular Structure**: Separated code into clear modules:
   - `models/`: ML models (classifier, LDA, sentiment)
   - `services/`: Business logic (data loading, retrieval, LLM, similarity)
   - `pipeline/`: Main RAG orchestration
   - `config/`: Centralized configuration

2. **Better Organization**: 
   - Each service has a single responsibility
   - Clear separation of concerns
   - Easy to test and maintain

3. **Documentation**: 
   - Comprehensive docstrings
   - Clear README files
   - Inline comments where needed

4. **Configuration**: 
   - Centralized settings in `config/settings.py`
   - Environment variable support
   - Easy to customize

### Frontend Improvements

1. **Component Organization**: 
   - Components grouped by purpose (Layout, Search, Content)
   - Reusable components
   - Clear component hierarchy

2. **State Management**: 
   - Better state organization
   - Error handling
   - Loading states

3. **Code Quality**: 
   - Consistent naming
   - Better comments
   - Improved accessibility

4. **Configuration**: 
   - API configuration separated
   - Environment variable support

## 📚 Key Features

- **RAG Pipeline**: Retrieval-Augmented Generation for answering security questions
- **Multiple Classifiers**: SVM for security category, LDA for topic classification
- **Sentiment Analysis**: VADER sentiment analysis on questions
- **Similarity Calculation**: Relevance and answer similarity metrics
- **Modern UI**: Clean, responsive React interface
- **Fast Search**: Instant search with loading states

## 🔧 Configuration

Both backend and frontend support environment variables for configuration. See individual README files for details.

## 📝 Notes

- Ensure all data files are in the correct directories
- The SVM classifier model should be in `rag-backend/app/models/svm_classifier.joblib`
- LDA models should be in `rag-backend/data/LDA_doc/`
- CSV data should be in `rag-backend/data/`

## 🎯 Next Steps

1. Copy your data files to the appropriate directories
2. Ensure the SVM classifier model is in place
3. Start the backend server
4. Start the frontend server
5. Begin searching!

