@echo off
chcp 65001 >nul
echo Starting backend service only...
echo.

cd rag-backend

if not exist "venv" (
    echo [ERROR] Virtual environment not found
    echo Please run start_local.bat first to create the environment
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [INFO] Starting backend on http://localhost:8000
echo [INFO] Press Ctrl+C to stop
echo.

uvicorn app.main:app --reload --port 8000

