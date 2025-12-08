@echo off
chcp 65001 >nul
echo Checking Ollama status...
echo.

echo [1] Checking if Ollama is running...
tasklist /FI "IMAGENAME eq ollama.exe" 2>nul | find /I "ollama.exe" >nul
if errorlevel 1 (
    echo [ERROR] Ollama is not running!
    echo Please start Ollama from Start Menu or run: ollama serve
) else (
    echo [OK] Ollama process is running
)
echo.

echo [2] Checking if llama3 model is available...
ollama list 2>nul | findstr /C:"llama3" >nul
if errorlevel 1 (
    echo [ERROR] llama3 model not found!
    echo Please run: ollama pull llama3
) else (
    echo [OK] llama3 model is available
)
echo.

echo [3] Testing Ollama connection...
powershell -Command "$ErrorActionPreference='Stop'; try { $r = Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -TimeoutSec 5; Write-Host '[OK] Ollama API is responding'; Write-Host 'Status:' $r.StatusCode } catch { Write-Host '[ERROR] Ollama API connection failed:'; Write-Host $_.Exception.Message }"
echo.

echo [4] Testing simple chat request...
powershell -Command "$ErrorActionPreference='Stop'; try { $body = @{model='llama3'; prompt='Hello'; stream=$false} | ConvertTo-Json; $r = Invoke-WebRequest -Uri 'http://localhost:11434/api/generate' -Method POST -Body $body -ContentType 'application/json' -TimeoutSec 30; Write-Host '[OK] Ollama chat test successful'; Write-Host 'Status:' $r.StatusCode } catch { Write-Host '[ERROR] Ollama chat test failed:'; Write-Host $_.Exception.Message }"
echo.

echo ================================================
echo Recommendations:
echo ================================================
echo 1. If Ollama is not running, start it from Start Menu
echo 2. If llama3 model is missing, run: ollama pull llama3
echo 3. If Ollama keeps crashing, try:
echo    - Close other heavy applications
echo    - Restart Ollama completely
echo    - Check system memory (Ollama needs ~4GB RAM for llama3)
echo 4. The backend now has delays between requests to prevent overload
echo.

pause

