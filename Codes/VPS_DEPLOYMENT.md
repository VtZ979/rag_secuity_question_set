# 🚀 VPS Deployment Guide

This guide explains how to deploy the RAG project on a VPS server.

## Prerequisites

- Linux VPS (Ubuntu/Debian recommended)
- Python 3.11+
- Node.js 18+
- Ollama installed and running
- Llama3 model downloaded
- Root or sudo access

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd OS1B-main/Codes
```

### 2. Make Scripts Executable

```bash
chmod +x deploy_vps.sh
chmod +x stop_deployment.sh
```

### 3. Configure Environment Variables (Optional)

#### Backend CORS Configuration

Edit `rag-backend/app/main.py` or set environment variable:

```bash
export ALLOWED_ORIGINS="https://your-domain.com,https://www.your-domain.com"
```

#### Frontend API URL

Edit `rag-frontend/.env.production`:

```env
VITE_API_URL=http://your-vps-ip:8001
# Or use domain:
# VITE_API_URL=https://api.your-domain.com
```

### 4. Run Deployment Script

```bash
./deploy_vps.sh
```

The script will:
1. Stop any existing deployment on port 8001
2. Set up backend environment
3. Build frontend for production
4. Start backend service on port 8001
5. Optionally start frontend preview server

## Deployment Details

### Port Configuration

- **Backend API**: Port 8001
- **Frontend Preview**: Port 5173 (optional, for testing)

### Service Management

#### Stop Deployment

```bash
./stop_deployment.sh
```

#### Check Service Status

```bash
# Check if backend is running
curl http://localhost:8001/

# Check logs
tail -f logs/backend.log

# Check process
ps aux | grep uvicorn
```

#### Restart Deployment

```bash
./stop_deployment.sh
./deploy_vps.sh
```

## Production Setup with Systemd (Recommended)

For production, it's recommended to use systemd to manage the backend service.

### 1. Install Systemd Service

```bash
# Edit the service file with correct paths
sudo nano rag-backend/rag-backend-8001.service

# Update paths in the service file:
# - WorkingDirectory: Full path to rag-backend directory
# - Environment PATH: Full path to venv/bin
# - ExecStart: Full path to uvicorn

# Copy service file to systemd
sudo cp rag-backend/rag-backend-8001.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable rag-backend-8001
sudo systemctl start rag-backend-8001

# Check status
sudo systemctl status rag-backend-8001
```

### 2. Service Management Commands

```bash
# Start service
sudo systemctl start rag-backend-8001

# Stop service
sudo systemctl stop rag-backend-8001

# Restart service
sudo systemctl restart rag-backend-8001

# View logs
sudo journalctl -u rag-backend-8001 -f
```

## Frontend Deployment Options

### Option 1: Nginx (Recommended for Production)

1. Build frontend:
```bash
cd rag-frontend
npm run build
```

2. Configure Nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/OS1B-main/Codes/rag-frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to backend
    location /askQuestion {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

3. Update frontend API URL in `.env.production`:
```env
VITE_API_URL=https://your-domain.com
```

### Option 2: Vite Preview Server (Testing Only)

The deployment script can start a Vite preview server for testing, but this is not recommended for production.

## Environment Variables

### Backend

Set these before running the deployment script:

```bash
# CORS allowed origins (comma-separated)
export ALLOWED_ORIGINS="https://your-domain.com,https://www.your-domain.com"
```

### Frontend

Edit `rag-frontend/.env.production`:

```env
# Backend API URL
VITE_API_URL=http://your-vps-ip:8001
```

## Firewall Configuration

Make sure ports are open:

```bash
# Ubuntu/Debian
sudo ufw allow 8001/tcp
sudo ufw allow 5173/tcp  # If using preview server
sudo ufw allow 80/tcp     # If using Nginx
sudo ufw allow 443/tcp    # If using HTTPS

# Check status
sudo ufw status
```

## Troubleshooting

### Backend Not Starting

1. Check logs:
```bash
tail -f logs/backend.log
```

2. Check if port is in use:
```bash
lsof -i:8001
```

3. Check Ollama:
```bash
ollama list
ollama serve  # If not running
```

### Frontend Cannot Connect to Backend

1. Check backend is running:
```bash
curl http://localhost:8001/
```

2. Check CORS configuration in `rag-backend/app/main.py`

3. Check API URL in frontend `.env.production`

4. Check firewall rules

### Permission Errors

If you get permission errors:

```bash
# Make scripts executable
chmod +x deploy_vps.sh stop_deployment.sh

# Check file permissions
ls -la
```

## Monitoring

### Check Service Health

```bash
# Backend health check
curl http://localhost:8001/

# Expected response:
# {"message":"Hello, FastAPI!"}
```

### View Logs

```bash
# Backend logs
tail -f logs/backend.log

# Systemd logs (if using systemd)
sudo journalctl -u rag-backend-8001 -f
```

### Resource Usage

```bash
# Check process
ps aux | grep uvicorn

# Check memory
free -h

# Check disk
df -h
```

## Security Considerations

1. **Use HTTPS**: Set up SSL/TLS certificates (Let's Encrypt)
2. **Firewall**: Only open necessary ports
3. **CORS**: Configure specific allowed origins, not `*`
4. **Environment Variables**: Don't commit sensitive data
5. **User Permissions**: Run services with non-root user

## Updating Deployment

To update the deployment:

```bash
# Pull latest changes
git pull

# Stop existing deployment
./stop_deployment.sh

# Re-deploy
./deploy_vps.sh
```

## Notes

- First backend startup takes 2-3 minutes to load data
- First search query may take 20-60 seconds (normal)
- Backend runs on port 8001 (not 8000)
- Frontend should be built for production before deployment
- Consider using a process manager (PM2, systemd) for production

