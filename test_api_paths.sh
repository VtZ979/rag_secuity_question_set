#!/bin/bash

# API 路径测试脚本
# 用于验证前后端路径配置是否正确

echo "🧪 API 路径配置测试"
echo "===================="
echo ""

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 测试后端直接访问
echo -e "${YELLOW}[测试 1] 后端直接访问${NC}"
echo "测试: GET http://localhost:8001/"
if curl -s http://localhost:8001/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 后端根路径可访问${NC}"
    curl -s http://localhost:8001/ | head -3
else
    echo -e "${RED}✗ 后端未运行或无法访问${NC}"
    echo "  请确保后端服务在端口 8001 上运行"
fi

echo ""
echo -e "${YELLOW}[测试 2] 后端健康检查${NC}"
echo "测试: GET http://localhost:8001/health"
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 健康检查通过${NC}"
    curl -s http://localhost:8001/health
    echo ""
else
    echo -e "${RED}✗ 健康检查失败${NC}"
fi

echo ""
echo -e "${YELLOW}[测试 3] 后端 API 端点${NC}"
echo "测试: POST http://localhost:8001/askQuestion"
RESPONSE=$(curl -s -X POST http://localhost:8001/askQuestion \
     -H "Content-Type: application/json" \
     -d '{"question": "test"}' 2>&1)

if echo "$RESPONSE" | grep -q "error\|answer\|related_post"; then
    echo -e "${GREEN}✓ API 端点可访问${NC}"
    echo "响应预览:"
    echo "$RESPONSE" | head -5
else
    echo -e "${RED}✗ API 端点访问失败${NC}"
    echo "响应: $RESPONSE"
fi

echo ""
echo -e "${YELLOW}[测试 4] 通过 Vite Proxy 访问（需要前端运行）${NC}"
echo "测试: GET http://localhost:3000/api/health"
if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Vite Proxy 工作正常${NC}"
    curl -s http://localhost:3000/api/health
    echo ""
else
    echo -e "${YELLOW}⚠ Vite Proxy 测试跳过（前端可能未运行）${NC}"
    echo "  如果前端在运行，这应该返回健康状态"
fi

echo ""
echo -e "${YELLOW}[测试 5] 路径配置验证${NC}"

# 检查配置文件
echo "检查前端 API 配置..."
if grep -q "baseURL.*'/api'" "rag-frontend/src/config/api.js" 2>/dev/null; then
    echo -e "${GREEN}✓ 前端 baseURL 配置为 /api${NC}"
else
    echo -e "${RED}✗ 前端 baseURL 配置可能不正确${NC}"
fi

if grep -q "askQuestion.*'/askQuestion'" "rag-frontend/src/config/api.js" 2>/dev/null; then
    echo -e "${GREEN}✓ 前端 askQuestion 端点配置正确${NC}"
else
    echo -e "${RED}✗ 前端 askQuestion 端点配置可能不正确${NC}"
fi

echo ""
echo "检查 Vite Proxy 配置..."
if grep -q "target.*8001" "rag-frontend/vite.config.js" 2>/dev/null; then
    echo -e "${GREEN}✓ Vite Proxy 目标端口为 8001${NC}"
else
    echo -e "${RED}✗ Vite Proxy 目标端口可能不正确${NC}"
fi

if grep -q "rewrite.*replace.*'/api'" "rag-frontend/vite.config.js" 2>/dev/null; then
    echo -e "${GREEN}✓ Vite Proxy rewrite 规则配置正确${NC}"
else
    echo -e "${RED}✗ Vite Proxy rewrite 规则可能不正确${NC}"
fi

echo ""
echo "检查后端配置..."
if grep -q "API_PORT.*8001" "rag-backend/config/settings.py" 2>/dev/null; then
    echo -e "${GREEN}✓ 后端端口配置为 8001${NC}"
else
    echo -e "${RED}✗ 后端端口配置可能不正确${NC}"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}测试完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "路径流程验证:"
echo "  前端: /api + /askQuestion = /api/askQuestion"
echo "  Vite Proxy: /api/askQuestion → /askQuestion"
echo "  后端: POST /askQuestion ✓"
echo ""

