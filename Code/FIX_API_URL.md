# 🔧 Fix Frontend API URL

## Issue

The original `rag-frontend/src/services/searchService.js` uses the wrong API URL:
```javascript
'http://127.0.0.1:80/askQuestion'  // ❌ Wrong port
```

But the backend runs on port **8000**, not 80.

## Quick Fix

Edit `rag-frontend/src/services/searchService.js` and change line 14:

**Before:**
```javascript
const response = await axios.post(
  'http://127.0.0.1:80/askQuestion',
  { question: query },
  { headers: { 'Content-Type': 'application/json' } }
);
```

**After:**
```javascript
const response = await axios.post(
  'http://localhost:8000/askQuestion',  // ✅ Correct port
  { question: query },
  { headers: { 'Content-Type': 'application/json' } }
);
```

## Alternative: Use Vite Proxy

If you prefer to use a proxy (like in the current project), you can:

1. **Update `vite.config.js`:**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      }
    }
  }
})
```

2. **Update `searchService.js`:**
```javascript
const response = await axios.post(
  '/api/askQuestion',  // Use proxy
  { question: query },
  { headers: { 'Content-Type': 'application/json' } }
);
```

## Verification

After making the change, test the connection:
1. Start backend: `uvicorn app.main:app --reload --port 8000`
2. Start frontend: `npm run dev`
3. Open http://localhost:5173
4. Try a search query
5. Check browser console for errors

