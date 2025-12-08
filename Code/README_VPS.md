# 🚀 VPS 部署快速指南

## 一键部署

```bash
# 1. 设置权限
chmod +x deploy_vps.sh stop_deployment.sh

# 2. 配置前端 API 地址（重要！）
# 编辑 rag-frontend/.env.production，设置 VITE_API_URL=http://your-vps-ip:8001

# 3. 部署
./deploy_vps.sh
```

## 停止服务

```bash
./stop_deployment.sh
```

## 重要提示

1. **前端 API 配置**: 部署前必须配置 `rag-frontend/.env.production`
2. **Python 版本**: 支持 3.10-3.13，推荐 3.11
3. **首次启动**: 需要 2-3 分钟加载数据
4. **端口**: 后端 8001，前端 5173

详细文档请查看 `VPS_DEPLOYMENT_GUIDE.md`

