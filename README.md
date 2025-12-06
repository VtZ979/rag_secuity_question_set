# Augmented Security Knowledge Hub - Final Version

This is the refactored and cleaned-up version of the RAG-based security knowledge hub project. The code has been reorganized for better maintainability, clarity, and demonstration purposes.

## 📁 Project Structure

```
final version/
├── rag-backend/          # FastAPI backend
│   ├── app/
│   │   ├── main.py       # FastAPI application
│   │   ├── models/       # ML models (classifiers, analyzers)
│   │   ├── services/     # Business logic services
│   │   └── pipeline/     # RAG pipeline
│   ├── config/           # Configuration
│   ├── data/             # Data files (CSV, models)
│   ├── requirements.txt
│   └── README.md
│
└── rag-frontend/         # React frontend
    ├── src/
    │   ├── components/   # React components
    │   ├── config/       # Configuration
    │   ├── services/     # API services
    │   └── App.jsx       # Main app
    ├── package.json
    └── README.md
```

## 🚀 Quick Start

### 🛠️ 开发模式（推荐 - 使用 Vite Dev Server）

#### 快速启动（一键启动前后端）

**Linux/Mac:**
```bash
bash start_dev.sh
```

**Windows:**
```batch
start_dev.bat
```

#### 手动启动

**1. 启动后端（端口 8001）**
```bash
cd rag-backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**2. 启动前端（新终端，端口 3000）**
```bash
cd rag-frontend
npm install  # 首次运行
npm run dev
```

**访问地址:**
- 前端: http://localhost:3000
- 后端 API: http://localhost:8001
- API 文档: http://localhost:8001/docs

**说明:**
- 前端通过 Vite proxy 访问后端，API 请求会自动转发（`/api/*` → `http://localhost:8001/*`）
- 后端监听 `0.0.0.0:8001` 以允许外部访问
- CORS 已配置为允许 `localhost:3000`

### 📦 生产模式（使用 Nginx）

如果需要部署到生产环境，请参考 `deploy_vps.sh` 脚本。

## ✨ Improvements Made

### Backend Improvements

1. **Modular Structure**: Separated code into clear modules:
   - `models/`: ML models (classifier, LDA, sentiment)
   - `services/`: Business logic (data loading, retrieval, LLM, similarity)
   - `pipeline/`: Main RAG orchestration
   - `config/`: Centralized configuration

2. **Better Organization**: 
   - Each service has a single responsibility
   - Clear separation of concerns
   - Easy to test and maintain

3. **Documentation**: 
   - Comprehensive docstrings
   - Clear README files
   - Inline comments where needed

4. **Configuration**: 
   - Centralized settings in `config/settings.py`
   - Environment variable support
   - Easy to customize

### Frontend Improvements

1. **Component Organization**: 
   - Components grouped by purpose (Layout, Search, Content)
   - Reusable components
   - Clear component hierarchy

2. **State Management**: 
   - Better state organization
   - Error handling
   - Loading states

3. **Code Quality**: 
   - Consistent naming
   - Better comments
   - Improved accessibility

4. **Configuration**: 
   - API configuration separated
   - Environment variable support

## 📚 Key Features

- **RAG Pipeline**: Retrieval-Augmented Generation for answering security questions
- **Multiple Classifiers**: SVM for security category, LDA for topic classification
- **Sentiment Analysis**: VADER sentiment analysis on questions
- **Similarity Calculation**: Relevance and answer similarity metrics
- **Modern UI**: Clean, responsive React interface
- **Fast Search**: Instant search with loading states

## 🔧 Configuration

Both backend and frontend support environment variables for configuration. See individual README files for details.

## 📝 Notes

- Ensure all data files are in the correct directories
- The SVM classifier model should be in `rag-backend/app/models/svm_classifier.joblib`
- LDA models should be in `rag-backend/data/LDA_doc/`
- CSV data should be in `rag-backend/data/`

## 🎯 Next Steps

1. Copy your data files to the appropriate directories
2. Ensure the SVM classifier model is in place
3. Start the backend server
4. Start the frontend server
5. Begin searching!

## 🔄 更新 VPS 上的代码

如果你的代码已经部署在 VPS 上，可以使用以下方法更新：

### 方法 1: 使用更新脚本（推荐）

**在 VPS 上运行:**
```bash
cd /opt/security_answer_system  # 或你的项目目录
sudo bash update_vps.sh
```

### 方法 2: 手动更新

**步骤 1: 停止服务**
```bash
sudo systemctl stop security-answer-system-backend
```

**步骤 2: 更新代码**
```bash
cd /opt/security_answer_system
# 如果使用 Git
git pull
# 或者使用 scp 上传新代码
```

**步骤 3: 更新依赖**
```bash
# 后端
cd rag-backend
source venv/bin/activate
pip install -r requirements.txt

# 前端（如果需要）
cd ../rag-frontend
npm install
npm run build
```

**步骤 4: 重启服务**
```bash
sudo systemctl daemon-reload
sudo systemctl start security-answer-system-backend
sudo systemctl status security-answer-system-backend
```

**步骤 5: 检查服务状态**
```bash
# 查看服务日志
sudo journalctl -u security-answer-system-backend -f

# 测试 API
curl http://127.0.0.1:8001/health
```

### 方法 3: 使用 scp 上传代码

**从本地到 VPS:**
```bash
# 上传整个项目目录
scp -r current\ project\ copy/* user@your-vps-ip:/opt/security_answer_system/

# 或者只上传修改的文件
scp current\ project\ copy/rag-frontend/src/config/api.js user@your-vps-ip:/opt/security_answer_system/rag-frontend/src/config/
scp current\ project\ copy/rag-frontend/vite.config.js user@your-vps-ip:/opt/security_answer_system/rag-frontend/
scp current\ project\ copy/rag-backend/config/settings.py user@your-vps-ip:/opt/security_answer_system/rag-backend/config/
```

**然后在 VPS 上运行更新脚本或手动重启服务**

## ⚠️ 重要提示

1. **端口配置**: 默认后端端口已改为 **8001**
2. **CORS 配置**: 开发环境允许 `localhost:3000`，生产环境可通过环境变量配置
3. **超时设置**: API 超时时间已增加到 60 秒（LLM 响应可能较慢）
4. **Vite Proxy**: 前端通过 `/api` 路径访问后端，Vite 会自动代理到 `localhost:8001`

