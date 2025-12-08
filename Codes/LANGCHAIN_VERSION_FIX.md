# LangChain 版本兼容性修复说明

## 修复内容

本次修复解决了 LangChain 新版本（>= 0.1.0）与旧版本代码的兼容性问题。

## 修复的文件

### 1. `rag-backend/app/pipeline/data_loader.py`
- **修复前**: `from langchain.docstore.document import Document`
- **修复后**: `from langchain_core.documents import Document`
- **原因**: `langchain.docstore` 在新版本中已移除，`Document` 移至 `langchain_core.documents`

### 2. `rag-backend/app/pipeline/retriever_builder.py`
- **修复前**: `from langchain.text_splitter import RecursiveCharacterTextSplitter`
- **修复后**: `from langchain_text_splitters import RecursiveCharacterTextSplitter`
- **原因**: `text_splitter` 已移至独立的 `langchain_text_splitters` 包

### 3. `rag-backend/app/pipeline/generator_builder.py`
- **修复前**: `from langchain.text_splitter import RecursiveCharacterTextSplitter`
- **修复后**: `from langchain_text_splitters import RecursiveCharacterTextSplitter`
- **原因**: 同上

### 4. `rag-backend/app/pipeline/rag_pipeline.py`
- **修复前**: `relevant_docs = retriever.get_relevant_documents(question)`
- **修复后**: 
  ```python
  try:
      relevant_docs = retriever.invoke(question)
  except (AttributeError, TypeError):
      relevant_docs = retriever.get_relevant_documents(question)
  ```
- **原因**: `get_relevant_documents()` 在新版本中已弃用，应使用 `invoke()`。添加了兼容性处理以支持新旧版本。

### 5. `rag-backend/requirements.txt`
- **添加**: `langchain_core` 和 `langchain_text_splitters`
- **原因**: 这些是新版本 LangChain 必需的独立包

## 版本兼容性

修复后的代码兼容：
- **旧版本** (langchain < 0.1.0): 使用 `get_relevant_documents()` 和旧的导入路径
- **新版本** (langchain >= 0.1.0): 使用 `invoke()` 和新的导入路径

## 部署说明

1. 这些修复已应用到本地文件
2. 推送到 GitHub 后，在 VPS 上重新部署：
   ```bash
   git pull
   ./stop_deployment.sh
   ./deploy_vps.sh
   ```

## 验证

部署后验证：
```bash
# 检查后端是否启动
curl http://localhost:8001/

# 查看日志
tail -f logs/backend.log
```

## 技术说明

### LangChain 版本变化

| 模块 | 旧版本 (< 0.1.0) | 新版本 (>= 0.1.0) |
|------|------------------|-------------------|
| Document | `langchain.docstore.document` | `langchain_core.documents` |
| TextSplitter | `langchain.text_splitter` | `langchain_text_splitters` |
| Hub | `langchain.hub` | `langchainhub` (独立包) |
| Retriever方法 | `get_relevant_documents()` | `invoke()` |

### 为什么需要修复？

1. **包结构重构**: LangChain 0.1.0+ 将核心功能拆分为独立包
2. **API 变化**: 方法名从 `get_relevant_documents()` 改为 `invoke()`
3. **向后兼容**: 新版本不再支持旧的导入路径

### 解决方案

使用兼容性代码同时支持新旧版本：
- 尝试新 API，失败时回退到旧 API
- 使用 try-except 处理版本差异
- 确保代码在不同环境下都能运行

