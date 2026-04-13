# ProctorForge AI - Local Development & Testing Guide

## Overview

This guide provides step-by-step instructions to run ProctorForge AI locally on your machine, verify that both frontend and backend are working correctly, and prepare for deployment to Vercel and Railway.

## Prerequisites

Before starting, ensure you have installed:

- **Node.js 18+** and **npm** (for frontend)
  - Download: https://nodejs.org/
  - Verify: `node --version` and `npm --version`

- **Python 3.10+** (for backend)
  - Download: https://www.python.org/
  - Verify: `python --version`

- **Git** (for version control)
  - Download: https://git-scm.com/
  - Verify: `git --version`

- **Optional: Docker & Docker Compose** (for containerized local development)
  - Download: https://www.docker.com/products/docker-desktop
  - Verify: `docker --version` and `docker-compose --version`

## Option 1: Non-Containerized Local Setup (Recommended for Development)

### Step 1: Clone the Repository

```bash
git clone https://github.com/rishi-0111/api-for-assignment-management-system.git
cd api-for-assignment-management-system
```

### Step 2: Setup Backend

#### 2.1 Navigate to Backend Directory

```bash
cd backend
```

#### 2.2 Create Python Virtual Environment

```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python -m venv venv
source venv/bin/activate
```

#### 2.3 Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 2.4 Create Local Environment File

```bash
# Copy the example env file
cp .env.example .env.local

# Edit .env.local with your settings (use default values for local testing)
# For local development with SQLite (default in .env.local): no changes needed
```

#### 2.5 Start Backend Server

```bash
# Option A: Run directly with Python
python main.py

# Option B: Run with Uvicorn (if you prefer)
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     reload watches directories ...
```

#### 2.6 Verify Backend is Running

Open in your browser:
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health (should return `{"status":"healthy", "service":"proctorforge-backend"}`)

### Step 3: Setup Frontend

#### 3.1 Open New Terminal Window

Keep the backend running in its terminal. In a new terminal, navigate to the project root.

#### 3.2 Navigate to Frontend Directory

```bash
cd frontend
```

#### 3.3 Install Node Dependencies

```bash
npm install
```

#### 3.4 Create Local Environment File

```bash
# Copy the example env file
cp .env.example .env.local

# For local development, the defaults in .env.local are correct:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

#### 3.5 Start Frontend Server

```bash
npm run dev
```

**Expected Output:**
```
  Local:        http://localhost:3000
  - Local:        http://127.0.0.1:3000
```

### Step 4: Verify Full Stack is Working

1. **Open http://localhost:3000 in your browser**
   - You should see the ProctorForge AI frontend
   - No server errors in browser console

2. **Check Network Communication**
   - Open browser DevTools (F12)
   - Go to Network tab
   - Try any action that calls the backend
   - You should see successful API calls to `http://localhost:8000`

3. **Check Backend Logs**
   - In the backend terminal, you should see request logs
   - Example: `GET /api/health HTTP/1.1" 200`

4. **Test Frontend-Backend Connection**
   - Navigate to login/register page
   - Try making a request (it should either succeed or show proper error handling)
   - Check browser console and server logs for any CORS or connection errors

## Option 2: Containerized Local Setup (Using Docker)

### Prerequisites

- Docker Desktop installed and running
- Docker Compose installed

### Step 1: Build and Run Containers

```bash
# From project root directory
docker-compose up -d
```

This will start:
- **PostgreSQL** on port 5432 (postgres:postgres)
- **Redis** on port 6379
- **Backend** on port 8000 (http://localhost:8000)
- **Frontend** on port 3000 (http://localhost:3000)

### Step 2: Verify Containers are Running

```bash
docker-compose ps
```

You should see all 4 services running (postgres, redis, backend, frontend).

### Step 3: Verify Services

- **Backend**: http://localhost:8000/api/health
- **Frontend**: http://localhost:3000
- **Backend Docs**: http://localhost:8000/docs

### Step 4: View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Step 5: Stop Containers

```bash
docker-compose down
```

## Testing the Integration

### Test 1: Frontend to Backend Connection

1. Open browser DevTools (F12)
2. Go to Console tab
3. Run this JavaScript command:
```javascript
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(d => console.log('Backend Response:', d))
  .catch(e => console.error('Error:', e))
```
4. You should see: `Backend Response: {status: 'healthy', service: 'proctorforge-backend'}`

### Test 2: WebSocket Connection (If Testing Live Features)

1. In browser console, run:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/exam/test');
ws.onopen = () => console.log('WebSocket connected');
ws.onerror = (e) => console.error('WebSocket error:', e);
ws.onclose = () => console.log('WebSocket closed');
```

### Test 3: Authentication Flow

1. Navigate to the login page
2. Submit credentials (if using test account)
3. Check browser Network tab to see API requests
4. Verify JWT token is stored in localStorage

## Troubleshooting

### Backend Won't Start

**Problem**: `ModuleNotFoundError: No module named ...`
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Problem**: `Port 8000 already in use`
```bash
# Solution: Use a different port
python main.py --port 8001

# Or find and kill the process using port 8000
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -i :8000
```

**Problem**: `SQLite database error`
```bash
# Solution: Delete the database file and restart
rm backend/proctorforge.db
python main.py
```

### Frontend Won't Start

**Problem**: `npm: command not found`
```bash
# Solution: Install Node.js from https://nodejs.org/
```

**Problem**: `Port 3000 already in use`
```bash
# Solution: Use a different port
npm run dev -- -p 3001
```

**Problem**: Blank page or build errors
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json .next
npm install
npm run dev
```

### Frontend Can't Connect to Backend

**Problem**: CORS error in console
```
Access to XMLHttpRequest from origin 'http://localhost:3000' has been blocked by CORS policy
```
**Solution**: 
1. Verify backend's `CORS_ORIGINS` includes `http://localhost:3000`
2. Check `.env.local` in backend has correct CORS settings
3. Restart backend

**Problem**: Backend URL not responding
```
GET http://localhost:8000/... - Failed to fetch
```
**Solution**:
1. Verify backend is running: http://localhost:8000/api/health
2. Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
3. Verify firewall isn't blocking port 8000

### Docker Issues

**Problem**: Container fails to start
```bash
# Check logs
docker-compose logs backend

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Problem**: Volume mounting issues
```bash
# Windows-specific: Ensure Docker has file sharing permissions
# Settings > Resources > File Sharing
```

## Next Steps: Prepare for Production Deployment

### 1. Create Production Environment Files

**Frontend (`frontend/.env.production`):**
```env
# Replace with your actual backend URL after Railway deployment
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
NEXT_PUBLIC_WS_URL=wss://your-backend-url.railway.app
```

**Backend (Railway will use environment variables)**

### 2. Test Production Builds Locally

**Frontend:**
```bash
cd frontend
npm run build
npm start  # This runs the production build
```

**Backend:**
```bash
cd backend
# Docker production build
docker build -t proctorforge-backend .
docker run -p 8000:8000 proctorforge-backend
```

### 3. Deploy to Railway & Vercel

Follow [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for:
- Deploying backend to Railway
- Deploying frontend to Vercel
- Connecting them together

## Performance Optimization

### Frontend Optimization

```bash
cd frontend

# Check bundle size
npm run build:analyze

# Generate lighthouse report
npm install -g lighthouse
lighthouse http://localhost:3000
```

### Backend Optimization

```bash
# Profile database queries
# Check SQLAlchemy logs for slow queries

# Test API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/health
```

## Debugging

### Backend Debugging with VS Code

1. Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

2. Set breakpoints and press F5 to debug

### Frontend Debugging

1. Use Chrome DevTools (F12)
2. Sources tab to set breakpoints
3. Console tab to run JavaScript
4. Network tab to inspect API calls

## Summary Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Backend health check returns 200
- [ ] Frontend can reach backend API
- [ ] No CORS errors in browser console
- [ ] No errors in backend terminal
- [ ] Database (SQLite) working locally
- [ ] Authentication flow working (if applicable)
- [ ] WebSocket connection working (if applicable)
- [ ] Production env files created
- [ ] Ready to deploy to Railway and Vercel

---

For deployment instructions, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
