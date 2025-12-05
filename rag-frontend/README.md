# Security Knowledge Base – Frontend

A modern React + Vite frontend for searching and viewing security-related questions from Stack Overflow. It provides instant search, LLM-generated summaries, skills/challenges tagging, and detailed post views.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
rag-frontend/
├── src/
│   ├── components/
│   │   ├── Layout/          # Layout components (Header, Footer, Breadcrumb)
│   │   ├── Search/          # Search components (SearchBox, TopicFilter)
│   │   └── Content/         # Content components (Hero, AnswerCard, PostDetail, etc.)
│   ├── config/              # Configuration files
│   │   └── api.js           # API configuration
│   ├── services/            # API services
│   │   └── api.js           # API client
│   ├── assets/              # Static assets
│   ├── App.jsx              # Main application component
│   ├── main.jsx             # Application entry point
│   └── index.css            # Global styles
├── public/                  # Public assets
├── index.html               # HTML template
├── package.json
├── vite.config.js
└── README.md
```

## 🎨 Tech Stack

| Technology | Description |
|------------|-------------|
| [React](https://reactjs.org/) | Component-based UI library |
| [Vite](https://vitejs.dev/) | Next-gen build tool with lightning-fast HMR |
| [Tailwind CSS](https://tailwindcss.com/) | Utility-first CSS framework |
| [daisyUI](https://daisyui.com/) | Tailwind UI components |
| [Axios](https://axios-http.com/) | HTTP client for API interaction |
| [Heroicons](https://heroicons.com/) | Icon library |

## ⚙️ Configuration

### API Configuration

Edit `src/config/api.js` to configure the API base URL:

```javascript
const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  // ...
};
```

Or set environment variable:

```bash
VITE_API_URL=http://your-api-url:8000 npm run dev
```

## 🔌 Features

- **Search Interface**: Clean search box with keyboard support
- **Topic Filters**: Quick access to popular security topics
- **Answer Display**: Structured display of LLM-generated answers
- **Related Posts**: List of related Stack Overflow questions
- **Post Details**: Detailed view of individual posts
- **Loading States**: Skeleton loaders during API calls
- **Error Handling**: User-friendly error messages

## 📝 Notes

- Ensure the backend API is running before starting the frontend
- The default API URL is `http://localhost:8000`
- CORS is configured on the backend to allow requests from the frontend

