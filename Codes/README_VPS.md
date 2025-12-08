# 🚀 VPS部署快速指南

## 快速开始

### 1. 在VPS上克隆仓库后，设置脚本权限

```bash
chmod +x deploy_vps.sh
chmod +x stop_deployment.sh
```

### 2. 配置环境变量（可选）

#### 前端API地址

编辑 `rag-frontend/.env.production`:

```env
VITE_API_URL=http://your-vps-ip:8001
```

#### 后端CORS配置

编辑 `rag-backend/app/main.py` 或设置环境变量：

```bash
export ALLOWED_ORIGINS="https://your-domain.com"
```

### 3. 运行部署脚本

```bash
./deploy_vps.sh
```

脚本会自动：
- ✅ 停止端口8001上的现有服务
- ✅ 设置后端环境
- ✅ 构建前端生产版本
- ✅ 启动后端服务（端口8001）
- ✅ 可选启动前端预览服务器

### 4. 停止部署

```bash
./stop_deployment.sh
```

## 重要说明

- **后端端口**: 8001（不是8000）
- **首次启动**: 需要2-3分钟加载数据
- **首次查询**: 可能需要20-60秒（正常现象）

## 详细文档

查看 `VPS_DEPLOYMENT.md` 获取完整部署指南。

