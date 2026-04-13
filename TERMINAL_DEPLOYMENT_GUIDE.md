# Terminal Commands - Complete Deployment Guide

This guide provides all the terminal commands needed to develop, test, and deploy your ProctorForge AI application.

---

## 📝 Before You Start

### 1. Verify Git is Installed and Connected
```bash
git --version
# Should show: git version 2.x.x

git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

### 2. Verify You Have the Code
```bash
# Navigate to your project
cd ai-assessment-main

# Check git remote
git remote -v
# Should show: origin https://github.com/rishi-0111/api-for-assignment-management-system.git

# Current branch
git branch
# Should show: * main
```

---

## 🖥️ Local Development Setup

### Step 1: Setup Backend (First Terminal)

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env.local for local development (copy from example)
# Windows:
copy .env.example .env.local
# macOS/Linux:
cp .env.example .env.local

# Start the backend server
python main.py

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**Verify Backend:**
```bash
# In a new terminal, test the health endpoint
curl http://localhost:8000/api/health

# Should return:
# {"status":"healthy","service":"proctorforge-backend"}

# View API documentation
# Open in browser: http://localhost:8000/docs
```

### Step 2: Setup Frontend (Second Terminal)

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Create .env.local for local development
# Windows:
copy .env.example .env.local
# macOS/Linux:
cp .env.example .env.local

# Start the frontend development server
npm run dev

# Expected output:
# - ready started server on 0.0.0.0:3000, url: http://localhost:3000
# - event compiled client and server successfully
```

**Verify Frontend:**
```bash
# In browser, visit: http://localhost:3000
# You should see the ProctorForge AI login page
```

### Step 3: Test Full Integration Locally

```bash
# In browser DevTools console (F12), test API connectivity:
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(d => console.log('Backend Response:', d))
  .catch(e => console.error('Error:', e))

# Expected output in console:
# Backend Response: {status: "healthy", service: "proctorforge-backend"}
```

---

## 🧪 Local Testing Workflows

### Testing Authentication

```bash
# Test User Registration (in browser DevTools or Postman)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "Password123!",
    "role": "student"
  }'

# Test User Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Password123!"
  }'

# Response should include:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "user": { "id": "...", "email": "test@example.com", ... }
# }
```

### Testing Protected Endpoints

```bash
# Get JWT token from login (copy the access_token value)
TOKEN="your-jwt-token-here"

# Test protected endpoint
curl -X GET http://localhost:8000/api/exams \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json"

# Should return list of exams or empty array
```

### Check Backend Logs

```bash
# The backend terminal shows all requests:
# INFO:     127.0.0.1:58234 - "GET /api/exams HTTP/1.1" 200 OK
# INFO:     127.0.0.1:58235 - "POST /api/auth/login HTTP/1.1" 200 OK
```

---

## 🚀 Production Deployment

### Step 1: Prepare Code for Deployment

```bash
# Navigate to project root
cd /path/to/ai-assessment-main

# Make sure everything is committed
git status
# Should show: "nothing to commit, working tree clean"

# If there are changes:
git add .
git commit -m "Prepare for production deployment"

# Push to GitHub
git push origin main

# Verify pushed
git log --oneline -1
# Should match the GitHub repo
```

### Step 2: Deploy Backend to Railway

#### Setup Railway

```bash
# Install Railway CLI (optional, can use dashboard)
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init

# Link project from dashboard:
# 1. Go to https://railway.app
# 2. Click "New Project"
# 3. Select "Deploy from GitHub Repo"
# 4. Select your repository
# 5. Set root directory: backend/
# 6. Click "Deploy"
```

#### Add Environment Variables to Railway

```bash
# In Railway dashboard, add:
# DATABASE_URL=postgresql+asyncpg://user:pass@host/db
# JWT_SECRET_KEY=<generate-strong-key>
# CORS_ORIGINS=http://localhost:3000

# Generate strong keys:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# View deployment logs
railway logs
```

#### Get Railway Backend URL

```bash
# In Railway dashboard:
# 1. Go to your project
# 2. Click "backend" service
# 3. Look for "Deployments" tab
# 4. Copy the generated URL (e.g., https://projectname-production.up.railway.app)

# Test it:
curl https://your-railway-backend-url/api/health
# Should return: {"status":"healthy","service":"proctorforge-backend"}
```

### Step 3: Deploy Frontend to Vercel

#### Setup Vercel

```bash
# Install Vercel CLI (optional, can use dashboard)
npm install -g vercel

# Deploy using CLI
vercel

# Or use dashboard:
# 1. Go to https://vercel.com
# 2. Click "Add New" → "Project"
# 3. Select your GitHub repository
# 4. Click "Import"
```

#### Configure Vercel for Monorepo

```bash
# In Vercel Settings:
# - Root Directory: frontend/
# - Build Command: npm run build
# - Output Directory: .next
# - Install Command: npm install
```

#### Add Environment Variables to Vercel

```bash
# In Vercel Project Settings → Environment Variables:
NEXT_PUBLIC_API_URL=https://your-railway-backend-url
NEXT_PUBLIC_WS_URL=wss://your-railway-backend-url

# Example:
# NEXT_PUBLIC_API_URL=https://proctorforge-prod.railway.app
# NEXT_PUBLIC_WS_URL=wss://proctorforge-prod.railway.app
```

#### Deploy Frontend

```bash
# Using CLI:
vercel --prod

# Or using dashboard:
# 1. Click "Deploy"
# 2. Wait for build to complete
# 3. Get your Vercel URL (e.g., https://projectname.vercel.app)
```

---

## 🔗 Post-Deployment Verification

### Step 1: Test Backend Health

```bash
# Replace URL with your Railway URL
curl https://your-railway-backend-url/api/health

# Expected response:
# {"status":"healthy","service":"proctorforge-backend"}
```

### Step 2: Update Backend CORS

```bash
# After getting Vercel URL, update Railway environment variable:
CORS_ORIGINS=https://your-vercel-app-url

# Example:
# CORS_ORIGINS=https://proctorforge-ai.vercel.app

# Railway will auto-redeploy with new CORS settings
```

### Step 3: Test Frontend

```bash
# Visit your Vercel frontend URL in browser
# https://your-app.vercel.app

# Open DevTools (F12) → Console
# Test API connectivity:
fetch('https://your-railway-backend-url/api/health')
  .then(r => r.json())
  .then(d => console.log('Connected!', d))

# Expected: Connected! {status: "healthy", service: "proctorforge-backend"}
```

### Step 4: Test Complete Flow

```bash
# 1. Go to login page
# 2. Try to register a user
# 3. Check DevTools → Network tab
# 4. See POST /api/auth/register
# 5. Should return 201 with token
# 6. Should redirect to dashboard
# 7. Dashboard should load exams from API
```

---

## 📊 Checking Deployment Logs

### Railway Backend Logs

```bash
# Using CLI:
railway logs --service backend

# Or in dashboard:
# 1. Go to https://railway.app
# 2. Select your project
# 3. Click "backend" service
# 4. Click "Logs" tab
# 5. Watch real-time logs

# Look for:
# ✅ INFO: Uvicorn running on 0.0.0.0:8000
# ✅ INFO: Application startup complete
# ❌ ERROR: (indicates problems)
```

### Vercel Frontend Logs

```bash
# Using CLI:
vercel logs

# Or in dashboard:
# 1. Go to https://vercel.com
# 2. Select your project
# 3. Click "Deployments" tab
# 4. Click on a deployment
# 5. Click "Logs"

# Look for:
# ✅ Build completed (shows build time)
# ✅ Ready (indicates successful deployment)
# ❌ FAILED (indicates build errors)
```

---

## 🔧 Common Commands Reference

### Git Commands

```bash
# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest
git pull origin main

# View commit history
git log --oneline
```

### Backend Commands

```bash
# Activate virtual environment (Windows)
cd backend && venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
cd backend && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Run tests
pytest

# View installed packages
pip list
```

### Frontend Commands

```bash
# Install dependencies
cd frontend && npm install

# Development server
npm run dev

# Production build
npm run build

# Run production build locally
npm start

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix
```

### Database Commands (for Railway)

```bash
# Connect to Railway PostgreSQL (if need to debug)
# Get credentials from Railway dashboard

psql postgresql://user:password@host:5432/proctorforge

# Common PostgreSQL commands:
\dt                    # List tables
SELECT * FROM users;   # Query users
\q                     # Quit
```

---

## 🧹 Cleanup & Maintenance

### Clearing Local Caches

```bash
# Backend cache
cd backend
rm -rf __pycache__
find . -type d -name __pycache__ -delete

# Frontend cache
cd frontend
rm -rf node_modules .next
npm cache clean --force

# Reinstall fresh
npm install
```

### Reset Local Database

```bash
# Remove SQLite database
cd backend
rm *.db

# Backend will recreate on next run
python main.py
```

### Monitoring Production

```bash
# View Railway logs in real-time
railway logs --service backend --tail

# View Vercel logs
vercel logs --follow

# Monitor uptime (add monitoring service)
# Recommend: UptimeRobot, Datadog, or New Relic
```

---

## ⚠️ Troubleshooting Commands

### Backend Won't Start

```bash
# Check Python version
python --version
# Need: Python 3.10+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port is available
# Windows:
netstat -ano | findstr :8000
# Kill process: taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
# Kill process: kill -9 <PID>
```

### Frontend Build Fails

```bash
# Clear all caches
cd frontend
rm -rf node_modules .next package-lock.json

# Reinstall
npm install

# Try building again
npm run build
```

### Database Connection Errors

```bash
# Test connection (replace credentials)
psql postgresql://user:password@host:5432/proctorforge

# If fails, check:
# 1. Credentials are correct
# 2. Host is accessible
# 3. Database exists
# 4. Network connectivity
```

### CORS Errors on Frontend

```bash
# Backend needs to allow frontend domain
# Update in Railway:
CORS_ORIGINS=https://your-vercel-app.vercel.app

# Railway auto-redeploys
# Force redeploy if needed: delete and re-add environment variable
```

---

## 🎯 Complete Deployment Checklist

### Pre-Deployment
- [ ] Code is clean and working locally
- [ ] All tests pass: `pytest` (backend)
- [ ] No console errors in frontend (`npm run dev`)
- [ ] Environment files ready (`.env.example` completed)
- [ ] Dependencies updated: `pip list`, `npm list`

### Deployment
- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] Environment variables set correctly
- [ ] Database migrations run
- [ ] CORS configured

### Post-Deployment
- [ ] Backend health check: `curl .../api/health` → 200
- [ ] Frontend loads without errors
- [ ] Login workflow works end-to-end
- [ ] Data persists after refresh
- [ ] API calls return correct data
- [ ] Real-time features work (if applicable)

### Monitoring
- [ ] Check logs daily for first week
- [ ] Monitor for errors
- [ ] Check performance metrics
- [ ] Plan rollback if needed

---

##  📞 Need Help?

| Issue | Command |
|-------|---------|
| Check backend status | `curl https://backend-url/api/health` |
| View backend logs | `railway logs --service backend` |
| View frontend logs | `vercel logs` |
| Test API endpoint | `curl https://backend-url/api/exams` |
| Check environment vars | `railway variables` (for backend) |
| Restart backend | Delete & re-add env var in Railway |
| Rebuild frontend | Push to GitHub → Vercel auto-builds |

---

**Deployment successful! Your app is now running on the internet! 🎉**
