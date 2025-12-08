# 🚀 Original RAG Project - Local Deployment Guide

## Quick Start

### Windows
```powershell
cd Codes
.\start_local.bat
```

### Linux/macOS
```bash
cd Codes
chmod +x start_dev.sh
./start_dev.sh
```

## Manual Setup

### Prerequisites
- Python 3.11.5
- Node.js (for frontend)
- Ollama + Llama3 model

### Backend Setup

1. **Install Ollama and Llama3**
   ```bash
   # Install Ollama from https://ollama.com/download
   ollama pull llama3
   ```

2. **Setup Python Environment**
   ```bash
   cd rag-backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

3. **Start Backend**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd rag-frontend
   npm install
   ```

2. **Start Frontend**
   ```bash
   npm run dev
   ```

## Important Notes

### API Configuration Issue

The original frontend code (`rag-frontend/src/services/searchService.js`) uses:
```javascript
'http://127.0.0.1:80/askQuestion'
```

But the backend runs on port **8000**, not 80. You have two options:

#### Option 1: Update Frontend Code (Recommended)
Edit `rag-frontend/src/services/searchService.js`:
```javascript
const response = await axios.post(
  'http://localhost:8000/askQuestion',  // Changed from :80 to :8000
  { question: query },
  { headers: { 'Content-Type': 'application/json' } }
);
```

#### Option 2: Use Proxy (Alternative)
Add proxy to `rag-frontend/vite.config.js`:
```javascript
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/askQuestion': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

Then update `searchService.js` to use relative path:
```javascript
const response = await axios.post(
  '/askQuestion',  // Relative path
  { question: query },
  { headers: { 'Content-Type': 'application/json' } }
);
```

## Ports

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173 (Vite default)

## Troubleshooting

### Backend Issues

1. **Ollama not found**
   - Install Ollama from https://ollama.com/download
   - Make sure Ollama is running: `ollama list`

2. **Llama3 model not found**
   - Download model: `ollama pull llama3`
   - This may take 10-20 minutes

3. **Import errors**
   - Make sure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **Initialization takes long time**
   - First startup loads data and models (2-3 minutes is normal)
   - Check backend logs for progress

### Frontend Issues

1. **Cannot connect to backend**
   - Check if backend is running on port 8000
   - Update API URL in `searchService.js` (see above)

2. **npm install fails**
   - Make sure Node.js is installed
   - Try: `npm cache clean --force` then `npm install`

## Stopping Services

### Windows
- Press `Ctrl+C` in each terminal window
- Or close the terminal windows

### Linux/macOS
- Press `Ctrl+C` in each terminal
- Or use: `kill <PID>` (PIDs shown when starting)

## Differences from Current Project

The original code structure:
- Backend uses port **8000** (not 8001)
- Frontend uses port **5173** (not 3000)
- No proxy configuration in Vite
- Simpler error handling
- Uses `get_relevant_documents()` (deprecated but works)

