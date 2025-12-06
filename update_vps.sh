#!/bin/bash

# VPS 更新脚本
# 使用方法: 在 VPS 上运行 bash update_vps.sh
# 或者在本地运行后通过 scp 上传到 VPS

set -e  # 遇到错误立即退出

echo "🔄 开始更新 VPS 上的代码..."

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量（根据你的实际情况修改）
PROJECT_DIR="/opt/security_answer_system"
SERVICE_NAME="security-answer-system-backend"
BACKEND_DIR="$PROJECT_DIR/rag-backend"
FRONTEND_DIR="$PROJECT_DIR/rag-frontend"
CURRENT_USER=$(logname || echo $SUDO_USER || whoami)

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}  VPS 代码更新脚本${NC}"
echo -e "${BLUE}  项目目录: $PROJECT_DIR${NC}"
echo -e "${BLUE}  服务名称: $SERVICE_NAME${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""

# 检查是否为root或sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}⚠️  建议使用 sudo 运行此脚本${NC}"
fi

# 第一步：备份当前代码
echo -e "${YELLOW}[1/6] 📦 备份当前代码...${NC}"
if [ -d "$PROJECT_DIR" ]; then
    BACKUP_DIR="${PROJECT_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
    echo "备份到: $BACKUP_DIR"
    cp -r "$PROJECT_DIR" "$BACKUP_DIR" 2>/dev/null || echo "备份失败，继续执行..."
    echo -e "${GREEN}✓ 备份完成${NC}"
else
    echo -e "${RED}❌ 项目目录不存在: $PROJECT_DIR${NC}"
    exit 1
fi

# 第二步：停止服务
echo -e "${YELLOW}[2/6] 🛑 停止服务...${NC}"
systemctl stop $SERVICE_NAME 2>/dev/null || echo "服务未运行"
echo -e "${GREEN}✓ 服务已停止${NC}"

# 第三步：更新代码（假设使用 git）
echo -e "${YELLOW}[3/6] 📥 更新代码...${NC}"
cd "$PROJECT_DIR"

if [ -d ".git" ]; then
    echo "从 Git 拉取最新代码..."
    sudo -u $CURRENT_USER git pull || git pull
    echo -e "${GREEN}✓ 代码更新完成${NC}"
else
    echo -e "${YELLOW}⚠️  未检测到 Git 仓库，请手动更新代码${NC}"
    echo "你可以："
    echo "  1. 使用 scp 上传新代码"
    echo "  2. 或者在此目录初始化 Git 仓库"
fi

# 第四步：更新后端依赖
echo -e "${YELLOW}[4/6] 🔧 更新后端依赖...${NC}"
cd "$BACKEND_DIR"
if [ -d "venv" ]; then
    sudo -u $CURRENT_USER bash -c "source venv/bin/activate && pip install -q --upgrade pip && pip install -q -r requirements.txt"
    echo -e "${GREEN}✓ 后端依赖更新完成${NC}"
else
    echo -e "${RED}❌ 虚拟环境不存在，请先运行部署脚本${NC}"
    exit 1
fi

# 第五步：重新构建前端（如果需要）
echo -e "${YELLOW}[5/6] 🎨 重新构建前端...${NC}"
cd "$FRONTEND_DIR"
if [ -d "node_modules" ]; then
    sudo -u $CURRENT_USER npm install --silent
    sudo -u $CURRENT_USER npm run build
    echo -e "${GREEN}✓ 前端构建完成${NC}"
else
    echo -e "${YELLOW}⚠️  node_modules 不存在，跳过前端构建${NC}"
fi

# 第六步：重启服务
echo -e "${YELLOW}[6/6] 🚀 重启服务...${NC}"
systemctl daemon-reload
systemctl start $SERVICE_NAME
sleep 3

# 检查服务状态
if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✓ 服务启动成功${NC}"
else
    echo -e "${RED}❌ 服务启动失败，请检查日志:${NC}"
    echo "  sudo journalctl -u $SERVICE_NAME -n 50"
    exit 1
fi

# 测试服务
echo ""
echo -e "${YELLOW}🧪 测试服务...${NC}"
sleep 2
if curl -s http://127.0.0.1:8001/health > /dev/null; then
    echo -e "${GREEN}✓ 后端健康检查通过${NC}"
else
    echo -e "${RED}⚠️  后端健康检查失败${NC}"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ 更新完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📝 有用的命令:${NC}"
echo "  查看服务状态: sudo systemctl status $SERVICE_NAME"
echo "  查看服务日志: sudo journalctl -u $SERVICE_NAME -f"
echo "  重启服务: sudo systemctl restart $SERVICE_NAME"
echo "  查看后端日志: sudo journalctl -u $SERVICE_NAME -n 100"
echo ""

