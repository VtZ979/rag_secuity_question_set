# 环境变量配置说明

## 前端环境变量

### 创建 `.env.production` 文件

在 `rag-frontend/` 目录下创建 `.env.production` 文件：

```env
# 后端 API 地址
# 替换为你的 VPS IP 地址或域名
VITE_API_URL=http://109.123.231.129:8001
```

### 示例配置

#### 本地开发
```env
VITE_API_URL=http://localhost:8000
```

#### VPS 部署（使用 IP）
```env
VITE_API_URL=http://109.123.231.129:8001
```

#### VPS 部署（使用域名）
```env
VITE_API_URL=https://api.your-domain.com
```

### 注意事项

1. **变量名必须以 `VITE_` 开头**，这是 Vite 的要求
2. **修改后需要重新构建前端**：
   ```bash
   cd rag-frontend
   npm run build
   ```
3. **生产环境使用 `.env.production`**，开发环境使用 `.env.local`

## 后端环境变量（可选）

### CORS 配置

如果需要手动配置 CORS，可以设置以下环境变量：

```bash
# VPS IP（自动检测，通常不需要手动设置）
export VPS_IP=109.123.231.129

# 额外的允许来源（用逗号分隔）
export ALLOWED_ORIGINS="https://your-domain.com,https://www.your-domain.com"
```

### 在部署脚本中设置

编辑 `deploy_vps.sh`，在启动后端前添加：

```bash
export VPS_IP=109.123.231.129
export ALLOWED_ORIGINS="https://your-domain.com"
```

## 验证配置

### 检查前端配置

构建后检查 `rag-frontend/dist` 中的代码，确认 API URL 正确。

### 检查后端 CORS

查看后端日志，确认允许的来源列表：

```bash
tail -f logs/backend.log | grep -i cors
```

