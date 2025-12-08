# ✅ 部署检查清单

在部署前，请确认以下所有项目：

## 📋 部署前检查

### 1. 代码准备
- [x] 所有 LangChain 兼容性修复已完成
- [x] requirements.txt 已固定版本
- [x] CORS 配置已更新
- [x] 前端 API 地址已配置为使用环境变量

### 2. 环境配置
- [ ] 已创建 `rag-frontend/.env.production` 文件
- [ ] `VITE_API_URL` 已设置为正确的 VPS IP 或域名
- [ ] Python 版本为 3.10-3.13（推荐 3.11）
- [ ] Node.js 已安装

### 3. 系统要求
- [ ] Ollama 已安装并运行
- [ ] Llama3 模型已下载（`ollama pull llama3`）
- [ ] 端口 8001 和 5173 未被占用
- [ ] 防火墙已允许相应端口

### 4. 脚本权限
- [ ] `deploy_vps.sh` 有执行权限（`chmod +x deploy_vps.sh`）
- [ ] `stop_deployment.sh` 有执行权限（`chmod +x stop_deployment.sh`）

## 🚀 部署步骤

1. **克隆/上传代码到 VPS**
   ```bash
   git clone <your-repo-url>
   cd <project-directory>/Code
   ```

2. **设置脚本权限**
   ```bash
   chmod +x deploy_vps.sh stop_deployment.sh
   ```

3. **配置前端环境变量**
   ```bash
   # 创建 .env.production 文件
   cd rag-frontend
   echo "VITE_API_URL=http://your-vps-ip:8001" > .env.production
   cd ..
   ```

4. **运行部署脚本**
   ```bash
   ./deploy_vps.sh
   ```

5. **等待部署完成**
   - 后端初始化需要 2-3 分钟
   - 观察日志输出确认无错误

6. **验证部署**
   ```bash
   # 检查后端
   curl http://localhost:8001/
   
   # 应该返回: {"message":"Hello, FastAPI!"}
   ```

## 🔍 部署后验证

### 后端验证
- [ ] `curl http://localhost:8001/` 返回 200 OK
- [ ] 后端日志无错误信息
- [ ] RAG 管道初始化成功

### 前端验证
- [ ] 前端可以访问（http://your-vps-ip:5173）
- [ ] 前端可以成功调用后端 API
- [ ] 搜索功能正常工作

### 功能测试
- [ ] 可以提交问题
- [ ] 可以收到回答
- [ ] 无 CORS 错误
- [ ] 无网络连接错误

## 🐛 常见问题

### 问题1: 后端无法启动
**解决方案**:
1. 检查日志: `tail -f logs/backend.log`
2. 检查依赖: `pip list | grep langchain`
3. 重新安装: `pip install -r requirements.txt --upgrade`

### 问题2: 前端无法连接后端
**解决方案**:
1. 确认 `.env.production` 中的 `VITE_API_URL` 正确
2. 重新构建前端: `cd rag-frontend && npm run build`
3. 检查 CORS 配置

### 问题3: 模块导入错误
**解决方案**:
1. 确认已安装所有依赖: `pip install -r requirements.txt`
2. 检查 Python 版本: `python3 --version`
3. 重新创建虚拟环境

## 📝 已修复的兼容性问题

- ✅ `langchain_core.pydantic_v1` 导入兼容性
- ✅ `langchain.docstore.document` → `langchain_core.documents`
- ✅ `langchain.text_splitter` → `langchain_text_splitters`
- ✅ `langchain.hub` → `langchainhub`
- ✅ `get_relevant_documents()` → `invoke()` 方法兼容性
- ✅ LangChain 版本固定为兼容组合

## 📚 相关文档

- `VPS_DEPLOYMENT_GUIDE.md` - 详细部署指南
- `README_VPS.md` - 快速开始指南
- `ENV_SETUP.md` - 环境变量配置说明

## 🎯 成功标准

部署成功的标志：
1. ✅ 后端服务在端口 8001 正常运行
2. ✅ 前端可以访问并正常显示
3. ✅ 可以成功提交问题并获得回答
4. ✅ 无错误日志
5. ✅ 所有 API 调用成功

---

**祝部署顺利！** 🎉

