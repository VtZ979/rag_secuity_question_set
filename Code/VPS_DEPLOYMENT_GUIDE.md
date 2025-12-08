# 🚀 稳定版本 VPS 部署指南

## 快速开始

### 1. 在 VPS 上克隆仓库后，设置脚本权限

```bash
cd Code
chmod +x deploy_vps.sh
chmod +x stop_deployment.sh
```

### 2. 配置前端 API 地址（重要！）

在部署前，编辑 `rag-frontend/.env.production` 文件（如果不存在则创建）：

```env
# 替换为你的 VPS IP 地址
VITE_API_URL=http://109.123.231.129:8001
```

或者使用域名：

```env
VITE_API_URL=https://api.your-domain.com
```

### 3. 运行部署脚本

```bash
./deploy_vps.sh
```

脚本会自动：
- ✅ 停止端口8001上的现有服务
- ✅ 设置后端环境并安装依赖
- ✅ 构建前端生产版本
- ✅ 启动后端服务（端口8001）
- ✅ 可选启动前端预览服务器

### 4. 停止部署

```bash
./stop_deployment.sh
```

## 重要配置说明

### 后端端口
- **默认端口**: 8001
- 可在 `deploy_vps.sh` 中修改 `BACKEND_PORT` 变量

### 前端配置

#### 方法1：使用环境变量（推荐）

创建 `rag-frontend/.env.production`：
```env
VITE_API_URL=http://your-vps-ip:8001
```

#### 方法2：直接修改代码

编辑 `rag-frontend/src/services/searchService.js`，修改 `API_BASE_URL` 的默认值。

### CORS 配置

后端会自动检测 VPS IP 并添加到 CORS 允许列表。如果需要手动配置：

1. 设置环境变量：
   ```bash
   export VPS_IP=109.123.231.129
   export ALLOWED_ORIGINS="https://your-domain.com,https://www.your-domain.com"
   ```

2. 或直接修改 `rag-backend/app/main.py` 中的 `origins` 列表

## 已修复的兼容性问题

### LangChain 版本兼容性
- ✅ `pydantic_v1` 导入兼容性
- ✅ `hub` 导入兼容性
- ✅ `Document` 导入兼容性
- ✅ `TextSplitter` 导入兼容性
- ✅ `get_relevant_documents` 方法兼容性

### 固定版本
- `langchain==0.0.354`
- `langchain_core==0.1.23`
- `langchain_community==0.0.20`
- `langchain_text_splitters==0.0.1`
- `langchainhub==0.1.14`

这些版本组合兼容新旧版本的 LangChain，确保代码可以正常运行。

## Python 版本要求

- **推荐**: Python 3.11（与稳定版本要求一致）
- **支持**: Python 3.10, 3.11, 3.12, 3.13
- **NumPy**: 自动适配（`numpy>=1.24.0,<1.27.0`）

## 部署后验证

### 1. 检查后端

```bash
# 健康检查
curl http://localhost:8001/

# 应该返回: {"message":"Hello, FastAPI!"}
```

### 2. 测试 API

```bash
curl -X POST http://localhost:8001/askQuestion \
  -H "Content-Type: application/json" \
  -d '{"question": "What is SQL injection?"}'
```

### 3. 查看日志

```bash
# 后端日志
tail -f logs/backend.log

# 前端日志（如果启动了预览服务器）
tail -f logs/frontend.log
```

### 4. 访问前端

在浏览器中访问：
- `http://your-vps-ip:5173/`（如果启动了预览服务器）
- 或配置 Nginx 服务 `rag-frontend/dist` 目录

## 故障排查

### 后端无法启动

1. **检查日志**:
   ```bash
   tail -n 100 logs/backend.log
   ```

2. **检查依赖**:
   ```bash
   cd rag-backend
   source venv/bin/activate
   pip list | grep langchain
   ```

3. **重新安装依赖**:
   ```bash
   pip install -r requirements.txt --upgrade --force-reinstall
   ```

### 前端无法连接后端

1. **检查 API 地址配置**:
   - 确认 `rag-frontend/.env.production` 中的 `VITE_API_URL` 正确
   - 确认构建时使用了正确的环境变量

2. **检查 CORS**:
   - 查看后端日志中的 CORS 错误
   - 确认前端域名在 CORS 允许列表中

3. **检查防火墙**:
   ```bash
   sudo ufw allow 8001/tcp
   sudo ufw allow 5173/tcp
   ```

### Ollama 相关问题

1. **检查 Ollama 状态**:
   ```bash
   ollama list
   ```

2. **启动 Ollama**:
   ```bash
   ollama serve
   ```

3. **下载模型**:
   ```bash
   ollama pull llama3
   ```

## 生产环境建议

### 1. 使用 Nginx 作为反向代理

配置 Nginx 服务前端并代理后端 API：

```nginx
# 前端
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/rag-frontend/dist;
    index index.html;
    location / {
        try_files $uri $uri/ /index.html;
    }
}

# 后端 API
server {
    listen 80;
    server_name api.your-domain.com;
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. 使用 systemd 管理服务

创建 systemd 服务文件（参考 `rag-backend/rag-backend-8001.service`）

### 3. 使用 HTTPS

配置 SSL 证书（Let's Encrypt）并更新 CORS 配置

## 更新部署

```bash
# 拉取最新代码
git pull

# 停止现有部署
./stop_deployment.sh

# 重新部署
./deploy_vps.sh
```

## 注意事项

1. **首次启动**: 后端需要 2-3 分钟加载数据
2. **首次查询**: 可能需要 20-60 秒（正常现象）
3. **环境变量**: 修改 `.env.production` 后需要重新构建前端
4. **端口冲突**: 确保端口 8001 和 5173 未被占用

## 技术支持

如果遇到问题：
1. 查看日志文件：`logs/backend.log`
2. 检查所有依赖是否正确安装
3. 确认 Ollama 和 Llama3 模型可用
4. 验证网络连接和防火墙设置

