#!/bin/bash

echo "========================================"
echo "Starting Original RAG Project"
echo "========================================"
echo

# Check directories
if [ ! -d "rag-backend" ]; then
    echo "[ERROR] rag-backend directory not found"
    echo "Please make sure you are running this script from the Codes directory"
    exit 1
fi

if [ ! -d "rag-frontend" ]; then
    echo "[ERROR] rag-frontend directory not found"
    echo "Please make sure you are running this script from the Codes directory"
    exit 1
fi

# Check Ollama
echo "[Check] Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "[WARNING] Ollama may not be installed"
    echo "Please install Ollama from https://ollama.com/download"
    read -p "Press Enter to continue anyway..."
else
    echo "[OK] Ollama is installed"
    
    # Check if Ollama is running
    if ollama list &> /dev/null; then
        echo "[OK] Ollama is running"
    else
        echo "[WARNING] Ollama may not be running"
        echo "Please start Ollama: ollama serve"
        read -p "Press Enter to continue anyway..."
    fi
    
    # Check Llama3
    echo "[Check] Checking Llama3 model..."
    if ollama list | grep -q "llama3"; then
        echo "[OK] Llama3 model found"
    else
        echo "[WARNING] Llama3 model not found"
        echo "Downloading Llama3 model (this may take 10-20 minutes)..."
        ollama pull llama3
        if [ $? -ne 0 ]; then
            echo "[ERROR] Failed to download Llama3"
            echo "Please manually run: ollama pull llama3"
            exit 1
        fi
    fi
fi

echo
echo "[1/2] Starting backend service..."
echo "Backend will run on http://localhost:8000"
echo

cd rag-backend

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        echo "Please install Python 3.11 or higher"
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

# Check dependencies
if [ ! -d "venv/lib/python*/site-packages/fastapi" ]; then
    echo "Installing backend dependencies..."
    echo "[Step 1] Upgrading pip..."
    pip install --upgrade pip --quiet
    echo "[Step 2] Installing setuptools and wheel..."
    pip install --upgrade setuptools wheel --quiet
    echo "[Step 3] Installing requirements..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        echo "Please check the error messages above"
        exit 1
    fi
fi

echo "Starting backend server..."
echo "[INFO] Backend will start in background"
echo "[INFO] Please wait for backend to initialize (this may take 2-3 minutes)"
nohup uvicorn app.main:app --reload --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "[INFO] Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "Waiting for backend to start (10 seconds for initialization)..."
sleep 10

# Test backend - try multiple times
echo "Testing backend connection..."
TEST_COUNT=0
while [ $TEST_COUNT -lt 10 ]; do
    TEST_COUNT=$((TEST_COUNT + 1))
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo "[OK] Backend is responding!"
        break
    else
        if [ $TEST_COUNT -lt 10 ]; then
            echo "[INFO] Backend not ready yet, waiting 5 more seconds... (attempt $TEST_COUNT/10)"
            sleep 5
        else
            echo "[WARNING] Backend may not have started successfully"
            echo "[INFO] Please check backend.log for errors"
            echo "[INFO] Backend initialization can take 2-3 minutes"
        fi
    fi
done

cd ..

echo
echo "[2/2] Starting frontend service..."
echo "Frontend will run on http://localhost:5173"
echo

cd rag-frontend

# Check node_modules
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install frontend dependencies"
        exit 1
    fi
fi

echo "Starting frontend development server..."
echo "[INFO] Frontend will start in background"
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "[INFO] Frontend PID: $FRONTEND_PID"

cd ..

echo
echo "========================================"
echo "[SUCCESS] Development environment started!"
echo "========================================"
echo
echo "Access URLs:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo
echo "Process IDs:"
echo "  Backend:  $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo
echo "Logs:"
echo "  Backend:  rag-backend/backend.log"
echo "  Frontend: rag-frontend/frontend.log"
echo
echo "Notes:"
echo "  - First backend startup takes 2-3 minutes to load data"
echo "  - First search may take 20-60 seconds (this is normal)"
echo "  - To stop services, run: kill $BACKEND_PID $FRONTEND_PID"
echo
echo "[IMPORTANT] Frontend API Configuration:"
echo "  The original code uses http://127.0.0.1:80/askQuestion"
echo "  You may need to update rag-frontend/src/services/searchService.js"
echo "  to use http://localhost:8000/askQuestion instead"
echo




