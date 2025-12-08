@echo off
chcp 65001 >nul
echo ========================================
echo Starting Original RAG Project
echo ========================================
echo.

REM Check directories
if not exist "rag-backend" (
    echo [ERROR] rag-backend directory not found
    echo Please make sure you are running this script from the Codes directory
    pause
    exit /b 1
)

if not exist "rag-frontend" (
    echo [ERROR] rag-frontend directory not found
    echo Please make sure you are running this script from the Codes directory
    pause
    exit /b 1
)

REM Check Ollama
echo [Check] Checking Ollama...
ollama list >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama may not be installed or running
    echo Please make sure Ollama is installed and running
    echo Visit https://ollama.com/download to download
    echo.
    pause
) else (
    echo [OK] Ollama is running
)

REM Check Llama3
echo [Check] Checking Llama3 model...
ollama list > temp_ollama_list.txt 2>&1
if errorlevel 1 (
    echo [DEBUG] Failed to get ollama list
    del temp_ollama_list.txt 2>nul
    goto check_llama3_done
)
findstr /C:"llama3" temp_ollama_list.txt >nul 2>&1
if errorlevel 1 goto llama3_not_found
echo [OK] Llama3 model found
goto cleanup_temp_file

:llama3_not_found
echo [WARNING] Llama3 model not found in list
echo [DEBUG] Available models:
type temp_ollama_list.txt
echo.
echo Downloading Llama3 model (this may take 10-20 minutes)...
ollama pull llama3
if errorlevel 1 (
    echo [ERROR] Failed to download Llama3
    echo Please manually run: ollama pull llama3
    del temp_ollama_list.txt 2>nul
    pause
    exit /b 1
)

:cleanup_temp_file
del temp_ollama_list.txt 2>nul
:check_llama3_done

echo.
echo [1/2] Starting backend service...
echo Backend will run on http://localhost:8000
echo.

cd rag-backend

REM Check virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        python3 -m venv venv
        if errorlevel 1 (
            echo [ERROR] Failed to create virtual environment
            echo Please install Python 3.11 or higher
            pause
            exit /b 1
        )
    )
)

REM Activate virtual environment and start
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    echo Please manually run: cd rag-backend ^&^& venv\Scripts\activate.bat ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check dependencies
if not exist "venv\Lib\site-packages\fastapi" (
    echo Installing backend dependencies...
    echo [Step 1] Upgrading pip...
    python -m pip install --upgrade pip --quiet
    echo [Step 2] Installing setuptools and wheel...
    python -m pip install --upgrade setuptools wheel --quiet
    echo [Step 3] Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        echo Please check the error messages above
        pause
        exit /b 1
    )
)

echo Starting backend server...
echo [INFO] Backend will start in a new window
echo [INFO] Please wait for backend to initialize (this may take 2-3 minutes)
start "Backend - Port 8000" cmd /k "cd /d %~dp0rag-backend && venv\Scripts\activate.bat && echo [INFO] Starting backend service... && echo [INFO] Access: http://localhost:8000 && echo [INFO] Press Ctrl+C to stop && echo [INFO] Initializing RAG pipeline (this may take 2-3 minutes)... && echo. && uvicorn app.main:app --reload --port 8000"

REM Wait for backend to start
echo Waiting for backend to start (10 seconds for initialization)...
timeout /t 10 /nobreak >nul

REM Test backend - try multiple times
echo Testing backend connection...
set TEST_COUNT=0
:test_backend_loop
set /a TEST_COUNT+=1
curl -s http://localhost:8000/ >nul 2>&1
if errorlevel 1 (
    if %TEST_COUNT% lss 11 (
        echo [INFO] Backend not ready yet, waiting 5 more seconds... (attempt %TEST_COUNT%/10)
        timeout /t 5 /nobreak >nul
        goto test_backend_loop
    ) else (
        echo [WARNING] Backend may not have started successfully
        echo [INFO] Please check the backend window for errors
        echo [INFO] Backend initialization can take 2-3 minutes
        echo [INFO] You can manually test: curl http://localhost:8000/
    )
) else (
    echo [OK] Backend is responding!
)

cd ..

echo.
echo [2/2] Starting frontend service...
echo Frontend will run on http://localhost:5173
echo.

cd rag-frontend

REM Check node_modules
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies
        pause
        exit /b 1
    )
)

echo Starting frontend development server...
start "Frontend - Port 5173" cmd /k "cd /d %~dp0rag-frontend && echo [OK] Frontend service is running... && echo Access: http://localhost:5173 && echo Press Ctrl+C to stop && echo. && npm run dev"

cd ..

echo.
echo ========================================
echo [SUCCESS] Development environment started!
echo ========================================
echo.
echo Access URLs:
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo.
echo Notes:
echo   - First backend startup takes 2-3 minutes to load data
echo   - First search may take 20-60 seconds (this is normal)
echo   - Closing windows will not stop services, press Ctrl+C in each window to stop
echo.
echo [IMPORTANT] Frontend API Configuration:
echo   The original code uses http://127.0.0.1:80/askQuestion
echo   You may need to update rag-frontend/src/services/searchService.js
echo   to use http://localhost:8000/askQuestion instead
echo.
pause

