# Security Knowledge Base – Frontend

A modern React + Vite frontend for searching and viewing security-related questions from Stack Overflow. It provides instant search, LLM-generated summaries, skills/challenges tagging, and detailed post views.

---

## Live Preview

> 🔗 Coming soon (deployment URL goes here)

---

## Tech Stack

| Technology | Description |
|------------|-------------|
| [React](https://reactjs.org/) | Component-based UI library |
| [Vite](https://vitejs.dev/) | Next-gen build tool with lightning-fast HMR |
| [Tailwind CSS](https://tailwindcss.com/) | Utility-first CSS framework |
| [daisyUI](https://daisyui.com/) | Tailwind UI components |
| [Axios](https://axios-http.com/) | HTTP client for API interaction |
| [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react) | React plugin with Fast Refresh support |

---

## Project Setup

### 1. Install dependencie

```bash
npm install
```
### 2. Start development server

```bash
npm run dev
```
### 3. Directory Structure
```bash
├── public/                        # Static public assets (served as-is)
│   ├── logo.svg
│   └── vite.svg
├── src/                           # Main application source code
│   ├── assets/                    # Internal static assets
│   │   ├── logo.svg
│   │   └── react.svg
│   ├── components/                # Reusable UI components
│   │   ├── Answer.jsx
│   │   ├── Filter.jsx
│   │   ├── Footer.jsx
│   │   ├── Header.jsx
│   │   ├── Hero.jsx
│   │   ├── OriginalQuestion.jsx
│   │   ├── PostContent.jsx
│   │   └── Skeleton.jsx
│   ├── data/                      # Mock or static data files
│   │   └── mockData.json
│   ├── services/                  # API service utilities
│   ├── App.jsx                    # Root component
│   ├── index.css                  # Global styles
│   └── main.jsx                   # React DOM rendering entry
├── dist/                          # Build output (auto-generated)
├── node_modules/                 # Project dependencies
└── package.json                  # Project manifest and scripts
```
