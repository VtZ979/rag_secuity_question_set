#!/bin/bash

###############################################################################
# VPS Production Deployment Script
# This script will:
# 1. Stop existing deployment on port 8001
# 2. Deploy backend to port 8001
# 3. Build and deploy frontend
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_PORT=8001
FRONTEND_PORT=5173
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/rag-backend"
FRONTEND_DIR="$PROJECT_DIR/rag-frontend"
SERVICE_NAME="rag-backend-8001"
LOG_DIR="$PROJECT_DIR/logs"
PID_FILE="$PROJECT_DIR/rag-backend-8001.pid"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}VPS Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Create logs directory
mkdir -p "$LOG_DIR"

###############################################################################
# Step 1: Stop existing deployment
###############################################################################
echo -e "${YELLOW}[Step 1/6] Stopping existing deployment on port $BACKEND_PORT...${NC}"

# Function to stop process on port
stop_port() {
    local port=$1
    local pid=$(lsof -ti:$port 2>/dev/null || echo "")
    
    if [ -n "$pid" ]; then
        echo "Found process $pid on port $port, stopping..."
        kill -9 $pid 2>/dev/null || true
        sleep 2
        echo -e "${GREEN}[OK] Port $port is now free${NC}"
    else
        echo "No process found on port $port"
    fi
}

# Stop port 8001
stop_port $BACKEND_PORT

# Stop systemd service if exists
if systemctl list-units --type=service | grep -q "$SERVICE_NAME"; then
    echo "Stopping systemd service: $SERVICE_NAME"
    sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
    sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true
fi

# Remove PID file if exists
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Stopping process from PID file: $OLD_PID"
        kill -9 "$OLD_PID" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
fi

echo -e "${GREEN}[OK] Existing deployment stopped${NC}"
echo ""

###############################################################################
# Step 2: Check prerequisites
###############################################################################
echo -e "${YELLOW}[Step 2/6] Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 is not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Python version: $PYTHON_VERSION"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}[ERROR] Node.js is not installed${NC}"
    exit 1
fi
NODE_VERSION=$(node --version)
echo "Node.js version: $NODE_VERSION"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}[WARNING] Ollama is not installed${NC}"
    echo "Please install Ollama from https://ollama.com/download"
else
    if ollama list &> /dev/null; then
        echo "Ollama is running"
        if ollama list | grep -q "llama3"; then
            echo "Llama3 model is available"
        else
            echo -e "${YELLOW}[WARNING] Llama3 model not found, downloading...${NC}"
            ollama pull llama3 || echo -e "${YELLOW}[WARNING] Failed to download Llama3${NC}"
        fi
    else
        echo -e "${YELLOW}[WARNING] Ollama is not running${NC}"
        echo "Please start Ollama: ollama serve"
    fi
fi

echo -e "${GREEN}[OK] Prerequisites checked${NC}"
echo ""

###############################################################################
# Step 3: Setup Backend
###############################################################################
echo -e "${YELLOW}[Step 3/6] Setting up backend...${NC}"

cd "$BACKEND_DIR"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install/upgrade dependencies
echo "Installing backend dependencies..."
pip install --upgrade setuptools wheel --quiet
pip install -r requirements.txt

echo -e "${GREEN}[OK] Backend setup complete${NC}"
echo ""

###############################################################################
# Step 4: Setup Frontend
###############################################################################
echo -e "${YELLOW}[Step 4/6] Setting up frontend...${NC}"

cd "$FRONTEND_DIR"

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
else
    echo "Updating frontend dependencies..."
    npm install
fi

# Build frontend for production
echo "Building frontend for production..."
npm run build

echo -e "${GREEN}[OK] Frontend setup complete${NC}"
echo ""

###############################################################################
# Step 5: Start Backend Service
###############################################################################
echo -e "${YELLOW}[Step 5/6] Starting backend service on port $BACKEND_PORT...${NC}"

cd "$BACKEND_DIR"
source venv/bin/activate

# Start backend in background
echo "Starting backend server..."
nohup uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT --no-reload > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!

# Save PID
echo $BACKEND_PID > "$PID_FILE"
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "Waiting for backend to initialize (this may take 2-3 minutes)..."
sleep 10

# Test backend connection
TEST_COUNT=0
MAX_TESTS=30
BACKEND_READY=false

while [ $TEST_COUNT -lt $MAX_TESTS ]; do
    TEST_COUNT=$((TEST_COUNT + 1))
    if curl -s http://localhost:$BACKEND_PORT/ > /dev/null 2>&1; then
        BACKEND_READY=true
        echo -e "${GREEN}[OK] Backend is responding!${NC}"
        break
    else
        if [ $TEST_COUNT -lt $MAX_TESTS ]; then
            echo "[INFO] Backend not ready yet, waiting 5 more seconds... (attempt $TEST_COUNT/$MAX_TESTS)"
            sleep 5
        fi
    fi
done

if [ "$BACKEND_READY" = false ]; then
    echo -e "${RED}[WARNING] Backend may not have started successfully${NC}"
    echo "Check logs: $LOG_DIR/backend.log"
    exit 1
fi

echo -e "${GREEN}[OK] Backend service started${NC}"
echo ""

###############################################################################
# Step 6: Start Frontend Service (Optional - using production build)
###############################################################################
echo -e "${YELLOW}[Step 6/6] Frontend deployment options...${NC}"

echo "Frontend has been built to: $FRONTEND_DIR/dist"
echo ""
echo "You have two options:"
echo "1. Use a web server (Nginx/Apache) to serve the built files"
echo "2. Use Vite preview server (for testing)"
echo ""

read -p "Start Vite preview server? (y/n) [n]: " START_PREVIEW
if [[ "$START_PREVIEW" =~ ^[Yy]$ ]]; then
    cd "$FRONTEND_DIR"
    echo "Starting Vite preview server on port $FRONTEND_PORT..."
    nohup npm run preview -- --port $FRONTEND_PORT --host > "$LOG_DIR/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    echo "Frontend PID: $FRONTEND_PID"
    echo -e "${GREEN}[OK] Frontend preview server started${NC}"
else
    echo "Skipping preview server. Configure your web server to serve: $FRONTEND_DIR/dist"
fi

echo ""

###############################################################################
# Deployment Summary
###############################################################################
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}[SUCCESS] Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Service URLs:"
echo "  Backend API:  http://$(hostname -I | awk '{print $1}'):$BACKEND_PORT"
echo "  Backend API:  http://localhost:$BACKEND_PORT"
if [[ "$START_PREVIEW" =~ ^[Yy]$ ]]; then
    echo "  Frontend:     http://$(hostname -I | awk '{print $1}'):$FRONTEND_PORT"
    echo "  Frontend:     http://localhost:$FRONTEND_PORT"
fi
echo ""
echo "Process Information:"
echo "  Backend PID:  $BACKEND_PID"
if [[ "$START_PREVIEW" =~ ^[Yy]$ ]]; then
    echo "  Frontend PID: $FRONTEND_PID"
fi
echo ""
echo "Logs:"
echo "  Backend:      $LOG_DIR/backend.log"
if [[ "$START_PREVIEW" =~ ^[Yy]$ ]]; then
    echo "  Frontend:     $LOG_DIR/frontend.log"
fi
echo ""
echo "Management Commands:"
echo "  Stop:         ./stop_deployment.sh"
echo "  View logs:    tail -f $LOG_DIR/backend.log"
echo "  Check status: curl http://localhost:$BACKEND_PORT/"
echo ""
echo -e "${YELLOW}Note:${NC} First backend startup takes 2-3 minutes to load data"
echo -e "${YELLOW}Note:${NC} First search may take 20-60 seconds (this is normal)"
echo ""

