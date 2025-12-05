#!/bin/bash

# OS1B项目VPS专用部署脚本
# 针对服务器: 109.123.231.129
# GitHub: https://github.com/VtZ979/rag_secuity_question_set
# 使用方法: sudo bash deploy_vps.sh

set -e  # 遇到错误立即退出

echo "🚀 开始部署OS1B项目到VPS (109.123.231.129)..."

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否为root或sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用sudo运行此脚本${NC}"
    exit 1
fi

# 配置变量
PROJECT_DIR="/opt/os1b"
BACKEND_DIR="$PROJECT_DIR/rag-backend"
FRONTEND_DIR="$PROJECT_DIR/rag-frontend"
CURRENT_USER=$(logname || echo $SUDO_USER || whoami)
GITHUB_REPO="https://github.com/VtZ979/rag_secuity_question_set.git"
VPS_IP="109.123.231.129"

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}  OS1B项目自动部署脚本${NC}"
echo -e "${BLUE}  VPS: $VPS_IP${NC}"
echo -e "${BLUE}  GitHub: $GITHUB_REPO${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""

# 第一步：更新系统
echo -e "${YELLOW}[1/12] 📦 更新系统包...${NC}"
apt update && apt upgrade -y

# 第二步：安装基础工具
echo -e "${YELLOW}[2/12] 📦 安装基础工具...${NC}"
apt install -y curl wget git build-essential software-properties-common

# 第三步：安装Python 3.11
echo -e "${YELLOW}[3/12] 🐍 安装Python 3.11...${NC}"
if ! command -v python3.11 &> /dev/null; then
    add-apt-repository ppa:deadsnakes/ppa -y
    apt update
    apt install -y python3.11 python3.11-venv python3.11-dev
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
    echo -e "${GREEN}✓ Python 3.11安装完成${NC}"
else
    echo -e "${GREEN}✓ Python 3.11已安装${NC}"
fi

# 第四步：安装Node.js
echo -e "${YELLOW}[4/12] 📦 安装Node.js...${NC}"
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt install -y nodejs
    echo -e "${GREEN}✓ Node.js安装完成${NC}"
else
    echo -e "${GREEN}✓ Node.js已安装 ($(node --version))${NC}"
fi

# 第五步：安装Nginx
echo -e "${YELLOW}[5/12] 🌐 安装Nginx...${NC}"
if ! command -v nginx &> /dev/null; then
    apt install -y nginx
    systemctl enable nginx
    systemctl start nginx
    echo -e "${GREEN}✓ Nginx安装完成${NC}"
else
    echo -e "${GREEN}✓ Nginx已安装${NC}"
fi

# 第六步：安装Ollama
echo -e "${YELLOW}[6/12] 🤖 安装Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
    systemctl enable ollama
    systemctl start ollama
    echo -e "${GREEN}✓ Ollama安装完成${NC}"
else
    echo -e "${GREEN}✓ Ollama已安装${NC}"
fi

# 第七步：下载LLaMA 3模型
echo -e "${YELLOW}[7/12] 📥 检查LLaMA 3模型...${NC}"
if ! sudo -u $CURRENT_USER ollama list 2>/dev/null | grep -q llama3; then
    echo -e "${YELLOW}⏳ 下载LLaMA 3模型（这可能需要10-20分钟，约4-5GB）...${NC}"
    sudo -u $CURRENT_USER ollama pull llama3 || ollama pull llama3
    echo -e "${GREEN}✓ LLaMA 3模型下载完成${NC}"
else
    echo -e "${GREEN}✓ LLaMA 3模型已存在${NC}"
fi

# 第八步：克隆项目
echo -e "${YELLOW}[8/12] 📥 克隆/更新项目代码...${NC}"
mkdir -p $PROJECT_DIR
chown $CURRENT_USER:$CURRENT_USER $PROJECT_DIR
cd $PROJECT_DIR

if [ -d ".git" ]; then
    echo -e "${YELLOW}更新现有代码...${NC}"
    sudo -u $CURRENT_USER git pull || git pull
else
    echo -e "${YELLOW}从GitHub克隆代码...${NC}"
    sudo -u $CURRENT_USER git clone $GITHUB_REPO . || git clone $GITHUB_REPO .
fi

# 检查项目结构
if [ -d "final version/rag-backend" ] && [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${YELLOW}检测到final version文件夹，复制到正确位置...${NC}"
    sudo -u $CURRENT_USER cp -r "final version/rag-backend" $PROJECT_DIR/ || cp -r "final version/rag-backend" $PROJECT_DIR/
    sudo -u $CURRENT_USER cp -r "final version/rag-frontend" $PROJECT_DIR/ || cp -r "final version/rag-frontend" $PROJECT_DIR/
fi

if [ ! -d "$BACKEND_DIR" ] || [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ 错误: 项目文件未找到！${NC}"
    echo -e "${YELLOW}请检查GitHub仓库结构${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 项目代码准备完成${NC}"

# 第九步：准备数据文件
echo -e "${YELLOW}[9/12] 📁 准备数据文件...${NC}"
cd $BACKEND_DIR
mkdir -p data/LDA_doc
mkdir -p app/models

# 检查数据文件
MISSING_FILES=0
if [ ! -f "data/StackOverflow_security_sample_labelled_all.csv" ]; then
    echo -e "${RED}⚠️  警告: CSV数据文件未找到！${NC}"
    MISSING_FILES=1
fi

if [ ! -f "data/LDA_doc/lda_model_best_7topics.model" ]; then
    echo -e "${RED}⚠️  警告: LDA模型文件未找到！${NC}"
    MISSING_FILES=1
fi

if [ ! -f "app/models/svm_classifier.joblib" ]; then
    echo -e "${RED}⚠️  警告: SVM分类器模型未找到！${NC}"
    MISSING_FILES=1
fi

if [ $MISSING_FILES -eq 1 ]; then
    echo -e "${YELLOW}请手动上传缺失的数据文件${NC}"
fi

# 第十步：设置后端环境
echo -e "${YELLOW}[10/12] 🔧 配置后端环境...${NC}"
if [ ! -d "venv" ]; then
    sudo -u $CURRENT_USER python3.11 -m venv venv
fi

sudo -u $CURRENT_USER bash -c "source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
echo -e "${GREEN}✓ 后端环境配置完成${NC}"

# 第十一步：构建前端
echo -e "${YELLOW}[11/12] 🎨 构建前端...${NC}"
cd $FRONTEND_DIR
sudo -u $CURRENT_USER npm install
sudo -u $CURRENT_USER npm run build
echo -e "${GREEN}✓ 前端构建完成${NC}"

# 第十二步：配置Nginx
echo -e "${YELLOW}[12/12] 🌐 配置Nginx...${NC}"
cat > /etc/nginx/sites-available/os1b <<EOF
server {
    listen 443;
    server_name $VPS_IP;

    root $FRONTEND_DIR/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)\$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

ln -sf /etc/nginx/sites-available/os1b /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx
echo -e "${GREEN}✓ Nginx配置完成${NC}"

# 第十三步：创建Systemd服务
echo -e "${YELLOW}[13/13] ⚙️  配置Systemd服务...${NC}"
cat > /etc/systemd/system/os1b-backend.service <<EOF
[Unit]
Description=OS1B FastAPI Backend
After=network.target ollama.service

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
ExecStart=$BACKEND_DIR/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable os1b-backend
systemctl start os1b-backend
echo -e "${GREEN}✓ Systemd服务配置完成${NC}"

# 第十四步：配置防火墙
echo -e "${YELLOW}[14/14] 🔥 配置防火墙...${NC}"
ufw allow 443/tcp
ufw allow 22/tcp
ufw --force enable
echo -e "${GREEN}✓ 防火墙配置完成${NC}"

# 等待服务启动
sleep 5

# 检查服务状态
echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}  服务状态检查${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""
echo "=== Nginx状态 ==="
systemctl status nginx --no-pager -l | head -3
echo ""
echo "=== 后端服务状态 ==="
systemctl status os1b-backend --no-pager -l | head -5
echo ""
echo "=== Ollama状态 ==="
systemctl status ollama --no-pager -l | head -3

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ 部署完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}🌐 访问地址: http://$VPS_IP:443${NC}"
echo -e "${GREEN}🔌 后端API: http://$VPS_IP:443/api${NC}"
echo ""
echo -e "${YELLOW}📝 有用的命令:${NC}"
echo "  查看后端日志: sudo journalctl -u os1b-backend -f"
echo "  重启后端: sudo systemctl restart os1b-backend"
echo "  重启Nginx: sudo systemctl restart nginx"
echo "  更新代码: cd /opt/os1b && git pull && sudo systemctl restart os1b-backend"
echo ""
echo -e "${YELLOW}⚠️  重要提示:${NC}"
echo "  1. 确保数据文件已上传到 /opt/os1b/rag-backend/data/"
echo "  2. 确保SVM分类器已上传到 /opt/os1b/rag-backend/app/models/"
echo "  3. 首次启动可能需要2-3分钟加载数据"
echo "  4. 如果遇到问题，查看日志: sudo journalctl -u os1b-backend -n 50"
echo ""

