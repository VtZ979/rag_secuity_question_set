@echo off
echo 🚀 启动开发环境...

REM 启动后端
echo [1/2] 启动后端服务...
cd rag-backend
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
echo ✓ 后端服务启动在 http://localhost:8001
start "Backend" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动前端
echo [2/2] 启动前端服务...
cd ..\rag-frontend
if not exist node_modules (
    echo 安装前端依赖...
    call npm install
)
echo ✓ 前端服务启动在 http://localhost:3000
start "Frontend" cmd /k "npm run dev"

echo.
echo ════════════════════════════════════
echo ✅ 开发环境已启动！
echo ════════════════════════════════════
echo.
echo 前端: http://localhost:3000
echo 后端: http://localhost:8001
echo API 文档: http://localhost:8001/docs
echo.
echo 关闭此窗口不会停止服务，请在各自的窗口中按 Ctrl+C 停止
pause

