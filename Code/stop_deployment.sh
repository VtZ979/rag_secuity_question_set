#!/bin/bash

###############################################################################
# Stop VPS Deployment Script
# This script will stop all services running on port 8001
###############################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKEND_PORT=8001
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="rag-backend-8001"
PID_FILE="$PROJECT_DIR/rag-backend-8001.pid"

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Stopping RAG Deployment${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Function to stop process on port
stop_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null || echo "")
    
    if [ -n "$pids" ]; then
        echo "Found process(es) on port $port: $pids"
        for pid in $pids; do
            echo "Stopping process $pid..."
            kill -9 $pid 2>/dev/null || true
        done
        sleep 2
        echo -e "${GREEN}[OK] Port $port is now free${NC}"
    else
        echo "No process found on port $port"
    fi
}

# Stop port 8001
echo "Stopping services on port $BACKEND_PORT..."
stop_port $BACKEND_PORT

# Stop systemd service if exists
if systemctl list-units --type=service 2>/dev/null | grep -q "$SERVICE_NAME"; then
    echo "Stopping systemd service: $SERVICE_NAME"
    sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
    sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true
    echo -e "${GREEN}[OK] Systemd service stopped${NC}"
fi

# Stop process from PID file if exists
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Stopping process from PID file: $OLD_PID"
        kill -9 "$OLD_PID" 2>/dev/null || true
        echo -e "${GREEN}[OK] Process $OLD_PID stopped${NC}"
    fi
    rm -f "$PID_FILE"
    echo -e "${GREEN}[OK] PID file removed${NC}"
fi

# Stop any frontend preview servers (port 4173 is Vite preview default, 5173 is our custom port)
for port in 4173 5173; do
    FRONTEND_PIDS=$(lsof -ti:$port 2>/dev/null || echo "")
    if [ -n "$FRONTEND_PIDS" ]; then
        echo "Stopping frontend preview server on port $port..."
        for pid in $FRONTEND_PIDS; do
            kill -9 $pid 2>/dev/null || true
        done
        echo -e "${GREEN}[OK] Frontend preview server on port $port stopped${NC}"
    fi
done

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}[SUCCESS] All services stopped${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

