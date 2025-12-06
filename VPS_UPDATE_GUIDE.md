# 🔄 VPS 更新指南

本指南说明如何将本地修改后的代码更新到 VPS 服务器上。

## 📋 更新前准备

### 1. 确认修改的文件

本次更新主要修改了以下文件：

- ✅ `rag-frontend/src/config/api.js` - API 配置，统一使用 `/api` 路径
- ✅ `rag-frontend/vite.config.js` - Vite 配置，proxy 指向 8001 端口
- ✅ `rag-backend/config/settings.py` - 后端配置，端口改为 8001，CORS 允许 localhost:3000

### 2. 确认 VPS 上的项目路径

根据你的部署脚本，项目路径应该是：
```
/opt/security_answer_system
```

如果不同，请修改下面的命令中的路径。

## 🚀 更新方法

### 方法 1: 使用 Git（推荐，如果 VPS 上已配置 Git）

**在 VPS 上执行：**

```bash
# 1. 停止服务
sudo systemctl stop security-answer-system-backend

# 2. 进入项目目录
cd /opt/security_answer_system

# 3. 拉取最新代码
git pull

# 4. 更新后端依赖
cd rag-backend
source venv/bin/activate
pip install -r requirements.txt

# 5. 重新构建前端（如果需要）
cd ../rag-frontend
npm install
npm run build

# 6. 重启服务
cd /opt/security_answer_system
sudo systemctl daemon-reload
sudo systemctl start security-answer-system-backend

# 7. 检查服务状态
sudo systemctl status security-answer-system-backend
```

### 方法 2: 使用更新脚本

**步骤 1: 上传更新脚本到 VPS**

```bash
# 从本地上传更新脚本
scp "current project copy/update_vps.sh" user@your-vps-ip:/tmp/update_vps.sh
```

**步骤 2: 在 VPS 上运行**

```bash
# SSH 登录到 VPS
ssh user@your-vps-ip

# 运行更新脚本
sudo bash /tmp/update_vps.sh
```

### 方法 3: 使用 scp 上传修改的文件（最直接）

**从本地 Windows 上传文件到 VPS：**

```powershell
# 设置变量
$VPS_USER = "your-username"
$VPS_IP = "your-vps-ip"
$VPS_PATH = "/opt/security_answer_system"

# 上传前端配置文件
scp "current project copy\rag-frontend\src\config\api.js" ${VPS_USER}@${VPS_IP}:${VPS_PATH}/rag-frontend/src/config/api.js
scp "current project copy\rag-frontend\vite.config.js" ${VPS_USER}@${VPS_IP}:${VPS_PATH}/rag-frontend/vite.config.js

# 上传后端配置文件
scp "current project copy\rag-backend\config\settings.py" ${VPS_USER}@${VPS_IP}:${VPS_PATH}/rag-backend/config/settings.py
```

**然后在 VPS 上执行：**

```bash
# 1. 停止服务
sudo systemctl stop security-answer-system-backend

# 2. 更新后端依赖（如果需要）
cd /opt/security_answer_system/rag-backend
source venv/bin/activate
pip install -r requirements.txt

# 3. 重新构建前端
cd /opt/security_answer_system/rag-frontend
npm install
npm run build

# 4. 重启服务
sudo systemctl daemon-reload
sudo systemctl start security-answer-system-backend

# 5. 检查服务状态
sudo systemctl status security-answer-system-backend
```

### 方法 4: 使用 rsync（推荐，支持增量同步）

```bash
# 从本地同步到 VPS
rsync -avz --exclude 'node_modules' --exclude 'venv' --exclude '.git' \
  "current project copy/" user@your-vps-ip:/opt/security_answer_system/
```

## 🔍 验证更新

### 1. 检查服务状态

```bash
sudo systemctl status security-answer-system-backend
```

应该看到 `active (running)` 状态。

### 2. 检查后端健康

```bash
curl http://127.0.0.1:8001/health
```

应该返回：
```json
{"status": "healthy"}
```

### 3. 检查后端端口

```bash
netstat -tlnp | grep 8001
```

应该看到：
```
tcp  0  0  0.0.0.0:8001  0.0.0.0:*  LISTEN  <pid>/uvicorn
```

### 4. 查看服务日志

```bash
# 实时查看日志
sudo journalctl -u security-answer-system-backend -f

# 查看最近 50 行日志
sudo journalctl -u security-answer-system-backend -n 50
```

### 5. 测试 API

```bash
# 测试根路径
curl http://127.0.0.1:8001/

# 测试搜索 API
curl -X POST http://127.0.0.1:8001/askQuestion \
     -H "Content-Type: application/json" \
     -d '{"question": "How to prevent SQL injection?"}'
```

## 🐛 常见问题排查

### 问题 1: 服务启动失败

**检查日志：**
```bash
sudo journalctl -u security-answer-system-backend -n 100
```

**常见原因：**
- 端口被占用：`sudo lsof -i :8001`
- 依赖缺失：检查 `requirements.txt` 是否已安装
- 配置文件错误：检查 `config/settings.py` 语法

### 问题 2: API 返回 404

**检查：**
1. 后端是否在运行：`sudo systemctl status security-answer-system-backend`
2. 端口是否正确：`netstat -tlnp | grep 8001`
3. Nginx 配置是否正确（如果使用 Nginx）

### 问题 3: CORS 错误

**检查：**
1. `config/settings.py` 中的 `ALLOWED_ORIGINS` 配置
2. 前端请求的 URL 是否正确

### 问题 4: 前端无法连接后端

**检查：**
1. Vite proxy 配置是否正确（`vite.config.js`）
2. 后端是否监听 `0.0.0.0` 而不是 `127.0.0.1`
3. 防火墙是否开放端口

## 📝 更新后的配置说明

### 端口配置

- **后端端口**: `8001`（默认）
- **前端端口**: `3000`（开发模式）
- **Nginx 端口**: `8080` 或 `443`（生产模式）

### API 路径

- **开发模式**: 前端通过 `/api/*` 访问，Vite proxy 转发到 `http://localhost:8001/*`
- **生产模式**: 前端通过 `/api/*` 访问，Nginx proxy 转发到 `http://127.0.0.1:8001/*`

### CORS 配置

- **开发环境**: 允许 `http://localhost:3000` 和 `http://127.0.0.1:3000`
- **生产环境**: 可通过环境变量 `ALLOWED_ORIGINS` 配置

## 🔧 环境变量配置（可选）

如果需要自定义配置，可以在 VPS 上设置环境变量：

```bash
# 编辑 systemd 服务文件
sudo nano /etc/systemd/system/security-answer-system-backend.service
```

在 `[Service]` 部分添加：
```ini
Environment="API_PORT=8001"
Environment="ALLOWED_ORIGINS=http://localhost:3000,http://your-domain.com"
```

然后重新加载并重启：
```bash
sudo systemctl daemon-reload
sudo systemctl restart security-answer-system-backend
```

## ✅ 更新检查清单

- [ ] 代码已上传到 VPS
- [ ] 后端依赖已更新
- [ ] 前端已重新构建（如果需要）
- [ ] 服务已重启
- [ ] 服务状态正常
- [ ] 健康检查通过
- [ ] API 测试成功
- [ ] 前端可以正常搜索

## 📞 需要帮助？

如果遇到问题，请检查：
1. 服务日志：`sudo journalctl -u security-answer-system-backend -f`
2. Nginx 日志：`sudo tail -f /var/log/nginx/error.log`
3. 系统日志：`sudo dmesg | tail`

