#!/bin/bash

# 开发环境启动脚本
# 使用方法: bash start_dev.sh

echo "🚀 启动开发环境..."

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查后端目录
if [ ! -d "rag-backend" ]; then
    echo -e "${RED}❌ 错误: rag-backend 目录不存在${NC}"
    exit 1
fi

# 检查前端目录
if [ ! -d "rag-frontend" ]; then
    echo -e "${RED}❌ 错误: rag-frontend 目录不存在${NC}"
    exit 1
fi

# 启动后端
echo -e "${YELLOW}[1/2] 启动后端服务...${NC}"
cd rag-backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3.11 -m venv venv || python3 -m venv venv
fi

# 激活虚拟环境并启动
source venv/bin/activate
pip install -q -r requirements.txt

echo -e "${GREEN}✓ 后端服务启动在 http://localhost:8001${NC}"
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 检查后端是否启动成功
if ! curl -s http://localhost:8001/health > /dev/null; then
    echo -e "${RED}⚠️  警告: 后端可能未成功启动，请检查日志${NC}"
fi

# 启动前端
echo -e "${YELLOW}[2/2] 启动前端服务...${NC}"
cd ../rag-frontend

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

echo -e "${GREEN}✓ 前端服务启动在 http://localhost:3000${NC}"
npm run dev &
FRONTEND_PID=$!

# 等待用户中断
echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ 开发环境已启动！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "前端: http://localhost:3000"
echo "后端: http://localhost:8001"
echo "API 文档: http://localhost:8001/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 捕获中断信号
trap "echo ''; echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# 等待
wait

