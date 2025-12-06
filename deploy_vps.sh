#!/bin/bash

# Security Answer System VPS专用部署脚本
# 针对服务器: 109.123.231.129
# GitHub: https://github.com/VtZ979/rag_secuity_question_set
# 使用方法: sudo bash deploy_vps.sh

set -e  # 遇到错误立即退出

echo "🚀 开始部署Security Answer System到VPS (109.123.231.129)..."

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
PROJECT_DIR="/opt/security_answer_system"
BACKEND_DIR="$PROJECT_DIR/rag-backend"
FRONTEND_DIR="$PROJECT_DIR/rag-frontend"
CURRENT_USER=$(logname || echo $SUDO_USER || whoami)
GITHUB_REPO="https://github.com/VtZ979/rag_secuity_question_set.git"
VPS_IP="109.123.231.129"
SERVICE_NAME="security-answer-system-backend"

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}  Security Answer System 自动部署脚本${NC}"
echo -e "${BLUE}  VPS: $VPS_IP${NC}"
echo -e "${BLUE}  GitHub: $GITHUB_REPO${NC}"
echo -e "${BLUE}  项目目录: $PROJECT_DIR${NC}"
echo -e "${BLUE}  服务名称: $SERVICE_NAME${NC}"
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

# 检查是否已经在项目目录中（如果脚本在项目根目录运行）
if [ -f "deploy_vps.sh" ] && [ -d "rag-backend" ] && [ -d "rag-frontend" ]; then
    echo -e "${GREEN}✓ 检测到已在项目目录中${NC}"
    # 更新代码（如果有更新）
    if [ -d ".git" ]; then
        echo -e "${YELLOW}更新代码...${NC}"
        sudo -u $CURRENT_USER git pull || git pull
    fi
elif [ -d ".git" ]; then
    echo -e "${YELLOW}更新现有代码...${NC}"
    sudo -u $CURRENT_USER git pull || git pull
else
    echo -e "${YELLOW}从GitHub克隆代码...${NC}"
    sudo -u $CURRENT_USER git clone $GITHUB_REPO . || git clone $GITHUB_REPO .
fi

# 检查项目结构（GitHub仓库直接在根目录有rag-backend和rag-frontend）
if [ ! -d "$BACKEND_DIR" ] || [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ 错误: 项目文件未找到！${NC}"
    echo -e "${YELLOW}请检查GitHub仓库结构，应该包含:${NC}"
    echo -e "  - rag-backend/"
    echo -e "  - rag-frontend/"
    echo -e "${YELLOW}当前目录内容:${NC}"
    ls -la
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

# 检查SVM分类器（可能在pipeline目录，需要移动到models目录）
if [ ! -f "app/models/svm_classifier.joblib" ]; then
    if [ -f "app/pipeline/svm_classifier.joblib" ]; then
        echo -e "${YELLOW}发现SVM分类器在pipeline目录，移动到models目录...${NC}"
        mv app/pipeline/svm_classifier.joblib app/models/svm_classifier.joblib
        echo -e "${GREEN}✓ SVM分类器已移动到正确位置${NC}"
    else
        echo -e "${RED}⚠️  警告: SVM分类器模型未找到！${NC}"
        MISSING_FILES=1
    fi
fi

if [ $MISSING_FILES -eq 1 ]; then
    echo -e "${YELLOW}请手动上传缺失的数据文件${NC}"
fi

# 修复配置文件路径（BASE_DIR应该是rag-backend目录，不是上级目录）
echo -e "${YELLOW}修复配置文件路径...${NC}"
if [ -f "config/settings.py" ]; then
    # 修复BASE_DIR路径：从parent.parent.parent改为parent.parent
    sed -i 's/BASE_DIR = Path(__file__).resolve().parent.parent.parent/BASE_DIR = Path(__file__).resolve().parent.parent/' config/settings.py
    echo -e "${GREEN}✓ 配置文件路径已修复${NC}"
else
    echo -e "${RED}⚠️  警告: 配置文件未找到${NC}"
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
# 使用8080端口（避免443端口冲突）
NGINX_PORT=8080
NGINX_CONFIG_NAME="security_answer_system"
cat > /etc/nginx/sites-available/$NGINX_CONFIG_NAME <<EOF
server {
    listen $NGINX_PORT;
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

ln -sf /etc/nginx/sites-available/$NGINX_CONFIG_NAME /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx
echo -e "${GREEN}✓ Nginx配置完成${NC}"

# 第十三步：创建Systemd服务
echo -e "${YELLOW}[13/13] ⚙️  配置Systemd服务...${NC}"
cat > /etc/systemd/system/$SERVICE_NAME.service <<EOF
[Unit]
Description=Security Answer System FastAPI Backend
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
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME
echo -e "${GREEN}✓ Systemd服务配置完成${NC}"

# 第十四步：配置防火墙
echo -e "${YELLOW}[14/14] 🔥 配置防火墙...${NC}"
ufw allow $NGINX_PORT/tcp
ufw allow 22/tcp
ufw --force enable
echo -e "${GREEN}✓ 防火墙配置完成（开放端口$NGINX_PORT）${NC}"

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
systemctl status $SERVICE_NAME --no-pager -l | head -5
echo ""
echo "=== Ollama状态 ==="
systemctl status ollama --no-pager -l | head -3

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ 部署完成！${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}🌐 访问地址: http://$VPS_IP:$NGINX_PORT${NC}"
echo -e "${GREEN}🔌 后端API: http://$VPS_IP:$NGINX_PORT/api${NC}"
echo ""
echo -e "${YELLOW}📝 有用的命令:${NC}"
echo "  查看后端日志: sudo journalctl -u $SERVICE_NAME -f"
echo "  重启后端: sudo systemctl restart $SERVICE_NAME"
echo "  重启Nginx: sudo systemctl restart nginx"
echo "  更新代码: cd $PROJECT_DIR && git pull && sudo systemctl restart $SERVICE_NAME"
echo ""
echo -e "${YELLOW}⚠️  重要提示:${NC}"
echo "  1. 确保数据文件已上传到 $BACKEND_DIR/data/"
echo "  2. 确保SVM分类器已上传到 $BACKEND_DIR/app/models/"
echo "  3. 首次启动可能需要2-3分钟加载数据"
echo "  4. 如果遇到问题，查看日志: sudo journalctl -u $SERVICE_NAME -n 50"
echo ""

