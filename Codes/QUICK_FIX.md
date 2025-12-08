# 🔧 快速修复指南

## 问题：HTTP ERROR 502

### 原因
uvicorn 0.38.0 版本不支持 `--no-reload` 选项，导致后端启动失败。

### 解决方案

#### 方法1：重新部署（推荐）

```bash
# 1. 停止当前部署
./stop_deployment.sh

# 2. 重新部署（已修复脚本）
./deploy_vps.sh
```

#### 方法2：手动修复并重启

```bash
# 1. 停止当前进程
./stop_deployment.sh

# 2. 手动启动后端（使用修复后的命令）
cd rag-backend
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8001 > ../logs/backend.log 2>&1 &

# 3. 检查是否启动成功
sleep 5
curl http://localhost:8001/

# 4. 查看日志
tail -f ../logs/backend.log
```

### 验证

部署成功后，应该看到：

```bash
curl http://localhost:8001/
# 应该返回: {"message":"Hello, FastAPI!"}
```

### 如果仍有问题

1. **检查后端日志**：
   ```bash
   tail -f logs/backend.log
   ```

2. **检查端口占用**：
   ```bash
   lsof -i:8001
   ```

3. **检查Ollama**：
   ```bash
   ollama list
   ```

4. **检查防火墙**：
   ```bash
   sudo ufw status
   sudo ufw allow 8001/tcp  # 如果需要
   ```

