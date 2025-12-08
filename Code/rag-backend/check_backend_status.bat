@echo off
chcp 65001 >nul
echo Checking backend status...
echo.

echo [1] Checking if port 8000 is listening...
netstat -ano | findstr :8000
if errorlevel 1 (
    echo [ERROR] Port 8000 is not listening
    echo Backend may not be running
) else (
    echo [OK] Port 8000 is listening
)
echo.

echo [2] Testing backend connection...
powershell -Command "$ErrorActionPreference='Stop'; try { $r = Invoke-WebRequest -Uri 'http://localhost:8000/' -TimeoutSec 5; Write-Host '[OK] Backend is responding!'; Write-Host 'Status:' $r.StatusCode; Write-Host 'Response:' $r.Content } catch { Write-Host '[ERROR] Backend connection failed:'; Write-Host $_.Exception.Message }"
echo.

echo [3] Checking backend process...
tasklist /FI "IMAGENAME eq python.exe" | findstr python
echo.

echo [4] If backend is not responding, check the backend window for:
echo   - Initialization messages
echo   - Error messages
echo   - Whether it's stuck at a specific step
echo.

pause

