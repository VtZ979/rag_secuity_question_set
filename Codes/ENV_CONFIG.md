# 环境变量配置说明

## 前端环境变量

### 创建 `.env.production` 文件

在 `rag-frontend/` 目录下创建 `.env.production` 文件：

```env
# 后端API地址
# 本地开发使用: http://localhost:8000
# VPS部署使用: http://your-vps-ip:8001 或 https://api.your-domain.com
VITE_API_URL=http://localhost:8001
```

### 创建 `.env.local` 文件（本地开发）

在 `rag-frontend/` 目录下创建 `.env.local` 文件（此文件不会被提交到Git）：

```env
# 本地开发环境变量
VITE_API_URL=http://localhost:8000
```

## 后端环境变量

### CORS配置

可以通过环境变量设置允许的源：

```bash
export ALLOWED_ORIGINS="https://your-domain.com,https://www.your-domain.com,http://localhost:5173"
```

或者在 `rag-backend/app/main.py` 中直接修改 `ALLOWED_ORIGINS` 列表。

### 默认CORS配置

如果不设置环境变量，默认允许：
- `http://localhost:5173`
- `http://127.0.0.1:5173`
- `http://localhost:4173`

## 注意事项

1. `.env.production` 文件用于生产构建（`npm run build`）
2. `.env.local` 文件用于本地开发，不会被Git跟踪
3. 环境变量必须以 `VITE_` 开头才能在Vite中使用
4. 修改环境变量后需要重新构建前端：`npm run build`

