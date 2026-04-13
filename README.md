# ✅ ProctorForge AI - Production-Ready Deployment Guide

> **Your project is now properly separated and ready for production deployment!**
> 
> **Frontend on Vercel | Backend on Railway | All through APIs**

---

## 🎯 What You Have Now

Your project is **fully separated** into production-ready components:

```
📁 ai-assessment-main/
├── 📂 frontend/          ← Deploy to Vercel (UI Layer)
│   ├── src/app           (Next.js pages)
│   ├── src/components    (React components)
│   ├── src/lib/api.ts    (API calls to backend)
│   ├── .env.local        (Local config)
│   └── vercel.json       (Vercel deployment)
│
├── 📂 backend/           ← Deploy to Railway (API Layer)
│   ├── routers/          (API endpoints)
│   ├── models/           (Database models)
│   ├── services/         (Business logic)
│   ├── main.py           (FastAPI app)
│   ├── .env.local        (Local config)
│   ├── -env              (Production config)
│   └── railway.json      (Railway deployment)
│
├── 📄 PRODUCTION_DEPLOYMENT.md        ← ⭐ START HERE
├── 📄 TERMINAL_DEPLOYMENT_GUIDE.md    ← For command line steps
├── 📄 FRONTEND_BACKEND_INTEGRATION.md ← How they work together
├── 📄 LOCAL_SETUP.md                  ← For local testing
└── 📄 README.md                       ← This file
```

---

## 🚀 Quick Start - 3 Options

### Option A: Local Development (Fastest)

**Using the command line:**

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows or: source venv/bin/activate
pip install -r requirements.txt
python main.py
# Backend at: http://localhost:8000

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
# Frontend at: http://localhost:3000
```

**Test it:**
- Open http://localhost:3000
- API calls go to http://localhost:8000
- Everything works locally ✓

### Option B: Production on Vercel + Railway (Recommended)

**Using the dashboards (no terminal needed initially):**

1. **Deploy Backend to Railway** (5 minutes)
   - Go to https://railway.app
   - Click "New Project" → Import GitHub
   - Set root to `backend/`
   - Get your Railway URL

2. **Deploy Frontend to Vercel** (5 minutes)
   - Go to https://vercel.com
   - Click "Add New Project" → Import GitHub
   - Set root to `frontend/`
   - Add env var `NEXT_PUBLIC_API_URL` = Railway URL
   - Get your Vercel URL

3. **Connect Them**
   - Update Railway `CORS_ORIGINS` to include Vercel URL
   - Done! Your app is live ✓

### Option C: Using Terminal Commands

For detailed terminal commands, see **[TERMINAL_DEPLOYMENT_GUIDE.md](./TERMINAL_DEPLOYMENT_GUIDE.md)**

---

## 📚 Complete Documentation

### 🎬 Getting Started
- **[LOCAL_SETUP.md](./LOCAL_SETUP.md)** - Run locally with detailed steps
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Quick command reference

### 🚀 Production Deployment  
- **[PRODUCTION_DEPLOYMENT.md](./PRODUCTION_DEPLOYMENT.md)** - ⭐ **START HERE FOR DEPLOYMENT**
  - Railway backend setup (step-by-step)
  - Vercel frontend setup (step-by-step)
  - Environment variables explained
  - Testing checklist
  - Troubleshooting guide

### 🔗 How Everything Works Together
- **[FRONTEND_BACKEND_INTEGRATION.md](./FRONTEND_BACKEND_INTEGRATION.md)**
  - Architecture diagram
  - API communication flow
  - Database operations through APIs
  - Authentication & JWT tokens
  - API endpoints reference
  - Debugging guide

### 💻 Terminal Commands
- **[TERMINAL_DEPLOYMENT_GUIDE.md](./TERMINAL_DEPLOYMENT_GUIDE.md)**
  - All deployment commands
  - Local testing commands
  - Production deployment commands
  - Log viewing commands
  - Troubleshooting commands

---

## ✨ Key Features of Your Setup

### ✅ Properly Separated
- **Frontend** (Vercel): UI, pages, state management
- **Backend** (Railway): APIs, database, authentication
- **Database**: PostgreSQL (via Railway)
- **Cache**: Redis (optional, via Railway)

### ✅ API-First Architecture
- Frontend NEVER touches database directly
- All data flows through REST APIs
- All operations go through backend
- Secure and scalable

### ✅ Authentication Implemented
- User registration & login via `/api/auth/register` & `/api/auth/login`
- JWT token-based auth
- Protected routes (requires valid token)
- Automatic token refresh
- Logout clears session

### ✅ Production Ready
- CORS configured for Vercel
- Environment variables managed
- Dockerfile for containerization
- Database migrations
- Error handling
- Logging

---

## 🎯 What's Where

### Frontend (`frontend/` → Vercel)
```
Display UI                          ← React/Next.js
Accept User Input                   ← Forms
Send HTTP Requests                  ← To backend APIs
Store JWT Token                     ← In localStorage
Cache State                         ← Zustand
Show Results                        ← Tables, charts, etc.
```

### Backend (`backend/` → Railway)
```
Receive HTTP Requests               ← From Vercel
Validate Authentication             ← JWT verification
Query Database                      ← PostgreSQL
Apply Business Logic                ← Python/FastAPI
Return JSON Responses               ← To Vercel
```

### Database (Railway PostgreSQL)
```
Store Users                         ← Registration/Login
Store Exams                         ← Exam data
Store Attempts                      ← Student responses
Store Analytics                     ← Metrics
```

---

## 🔐 Security Implementation

```
User Browser (Frontend)
        ↓
   Registers/Logs in
        ↓
Backend generates JWT token
        ↓
Frontend stores in localStorage
        ↓
Frontend sends with all requests:
Authorization: Bearer <JWT_TOKEN>
        ↓
Backend verifies JWT signature
        ↓
Backend checks permissions
        ↓
Backend returns data or 401
        ↓
Frontend handles response
```

---

## 📊 API Communication Example

### Example: Get Exams

```
FRONTEND                           BACKEND
┌─────────────────────────────┐   ┌─────────────────────────────┐
│ User clicks "Exams"         │   │                             │
└────────────┬────────────────┘   └─────────────────────────────┘
             │
             │ GET /api/exams
             │ Header: Authorization: Bearer jwt...
             ├────────────────────────────────────────────────>
             │
             │                   Verify JWT token
             │                   Query database
             │                   Format response
             │
             │ Response: [exam1, exam2, exam3]
             │ Status: 200 OK
             │<─────────────────────────────────────────────────
             │
             ▼
        Display exams
```

---

## ✅ Complete Setup Verification

### ✓ Code Structure
- [x] Frontend in `/frontend` directory
- [x] Backend in `/backend` directory
- [x] API client configured (`frontend/src/lib/api.ts`)
- [x] CORS enabled in backend (`backend/main.py`)
- [x] Database models exist (`backend/models/`)
- [x] API routers ready (`backend/routers/`)

### ✓ Configuration
- [x] `.env.example` files created (frontend + backend)
- [x] `.env.local` files created (for local dev)
- [x] `vercel.json` added (deployment config)
- [x] `railway.json` added (deployment config)
- [x] `docker-compose.yml` updated (local testing)

### ✓ Deployment Ready
- [x] No hardcoded URLs (using env variables)
- [x] All database operations through APIs
- [x] CORS configured for production
- [x] JWT authentication implemented
- [x] Error handling in place
- [x] Logging configured

---

## 🚀 Deployment Steps

### Quick Deploy (5-10 minutes)

1. **Backend to Railway**
   ```
   1. Go to https://railway.app
   2. New Project → Deploy from GitHub
   3. Select repo, set root to backend/
   4. Add env variables
   5. Deploy!
   ```

2. **Frontend to Vercel**
   ```
   1. Go to https://vercel.com
   2. Add New → Project
   3. Import GitHub repo
   4. Set root to frontend/
   5. Add NEXT_PUBLIC_API_URL env variable
   6. Deploy!
   ```

**For detailed steps, see [PRODUCTION_DEPLOYMENT.md](./PRODUCTION_DEPLOYMENT.md)**

---

## 🧪 Testing Your Setup

### Test 1: Local Development Works
```bash
# Terminal 1
cd backend && python main.py

# Terminal 2
cd frontend && npm run dev

# Browser: http://localhost:3000 → works ✓
```

### Test 2: Frontend Connects to Backend
```bash
# In browser console (F12)
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(d => console.log(d))

# Expected: {status: "healthy", service: "proctorforge-backend"}
```

### Test 3: Authentication Works
```bash
# 1. Go to http://localhost:3000/register
# 2. Create account
# 3. Check browser console → no errors
# 4. Check Network tab → POST /api/auth/register status 201
# 5. Should redirect to dashboard ✓
```

### Test 4: Features Work End-to-End
```bash
# 1. Login
# 2. Create exam
# 3. View exam list
# 4. Edit exam
# 5. Delete exam
# 6. All should work ✓
```

---

## 📋 Files Overview

| File | Purpose |
|------|---------|
| **PRODUCTION_DEPLOYMENT.md** | 🌟 Complete deployment guide (START HERE) |
| **FRONTEND_BACKEND_INTEGRATION.md** | How frontend & backend communicate |
| **TERMINAL_DEPLOYMENT_GUIDE.md** | All command-line commands |
| **LOCAL_SETUP.md** | Local development guide |
| **QUICK_REFERENCE.md** | Quick command reference |
| **PROJECT_COMPLETION_SUMMARY.md** | Summary of changes made |
| **frontend/.env.example** | Frontend env template |
| **backend/.env.example** | Backend env template |
| **frontend/vercel.json** | Vercel deployment config |
| **backend/railway.json** | Railway deployment config |

---

## 🎯 Next Steps

### Immediate (Next 5 minutes)
1. Read [PRODUCTION_DEPLOYMENT.md](./PRODUCTION_DEPLOYMENT.md)
2. Test locally: `cd backend && python main.py` + `cd frontend && npm run dev`
3. Verify http://localhost:3000 loads

### Short Term (Next 30 minutes)
1. Deploy backend to Railway
2. Deploy frontend to Vercel
3. Update CORS settings
4. Test connection

### Medium Term (First week)
1. Monitor logs for errors
2. Test all features end-to-end
3. Load test
4. Set up monitoring/alerts

### Long Term (Ongoing)
1. Optimize performance
2. Scale as needed
3. Add new features
4. Maintain & update

---

## 📞 Troubleshooting Quick Links

| Problem | Solution |
|---------|----------|
| Frontend can't connect to backend | See [PRODUCTION_DEPLOYMENT.md - CORS section](./PRODUCTION_DEPLOYMENT.md#-cors-errors) |
| Backend won't start | See [TERMINAL_DEPLOYMENT_GUIDE.md - Troubleshooting](./TERMINAL_DEPLOYMENT_GUIDE.md#-troubleshooting-commands) |
| Deployment fails | See [PRODUCTION_DEPLOYMENT.md - Troubleshooting](./PRODUCTION_DEPLOYMENT.md#-troubleshooting) |
| JWT token errors | See [FRONTEND_BACKEND_INTEGRATION.md - Authentication](./FRONTEND_BACKEND_INTEGRATION.md#-authentication-implementation) |
| API not responding | See [TERMINAL_DEPLOYMENT_GUIDE.md - Checking logs](./TERMINAL_DEPLOYMENT_GUIDE.md#-checking-deployment-logs) |

---

## 🌐 Final Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       INTERNET                              │
└──────────┬──────────────────────────────────────┬────────────┘
           │                                      │
    HTTPS/JSON                              HTTPS/JSON
           │                                      │
           ▼                                      ▼
┌──────────────────────────┐        ┌──────────────────────────┐
│  VERCEL                  │        │  RAILWAY                 │
│  https://app.vercel.app  │        │  https://backend.rail... │
│                          │        │                          │
│ ✓ Next.js 16            │        │ ✓ FastAPI               │
│ ✓ React 19              │        │ ✓ PostgreSQL            │
│ ✓ Tailwind CSS          │        │ ✓ Redis                 │
│ ✓ Zustand Store         │        │ ✓ JWT Auth              │
│ ✓ Axios HTTP Client     │◄──────►│ ✓ CORS Enabled          │
│                          │        │                          │
│ Features:               │        │ APIs:                    │
│ • Login/Register        │        │ • /api/auth             │
│ • Dashboard             │        │ • /api/exams            │
│ • Create Exams          │        │ • /api/attempts         │
│ • Take Exams            │        │ • /api/monitoring       │
│ • View Results          │        │ • /api/code_execution   │
└──────────────────────────┘        └──────────────────────────┘
```

---

## ✨ You're All Set!

Your ProctorForge AI application is:
- ✅ **Properly separated** (frontend & backend independent)
- ✅ **Production ready** (configured for Vercel & Railway)
- ✅ **API-first** (all operations through REST APIs)
- ✅ **Secure** (JWT authentication, CORS)
- ✅ **Scalable** (deployed on cloud platforms)
- ✅ **Well documented** (multiple guides included)

---

## 📖 Documentation Map

```
START HERE ↓
    │
    PRODUCTION_DEPLOYMENT.md ←── Complete step-by-step
    │
    ├→ Need CLI commands? → TERMINAL_DEPLOYMENT_GUIDE.md
    ├→ Need to debug? → FRONTEND_BACKEND_INTEGRATION.md
    ├→ Need local setup? → LOCAL_SETUP.md
    └→ Need quick ref? → QUICK_REFERENCE.md
```

---

## 🚀 Ready to Deploy?

**→ [Read PRODUCTION_DEPLOYMENT.md](./PRODUCTION_DEPLOYMENT.md) NOW**

It has:
- Step-by-step Railway backend deployment
- Step-by-step Vercel frontend deployment
- All environment variables explained
- Complete testing checklist
- Comprehensive troubleshooting guide

---

**Your journey to production starts now! 🎉**

Questions? Check the relevant guide above.
Stuck? See the troubleshooting section.
Need help? Check the FAQ in each guide.

Good luck! 🚀


### 3. **Administrator Portal**
- **Class Management**: Create and manage groups (Classes, Years, Sections).
- **Student Directory**: Full control over student accounts and status (Active/Banned).
- **System Metrics**: High-level overview of global activity, active tests, and user stats.
- **Quick Navigation**: Tab-based routing for rapid system administration.

---

## 🏗️ Technical Stack

- **Frontend**: [Next.js 14](https://nextjs.org/), [Tailwind CSS](https://tailwindcss.com/), [GSAP](https://greensock.com/gsap/), [Zustand](https://github.com/pmndrs/zustand).
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12), [SQLAlchemy](https://www.sqlalchemy.org/).
- **AI/ML**: [MediaPipe](https://google.github.io/mediapipe/) (Computer Vision), Custom Heuristic Trust Engine.
- **Real-time**: WebSockets for live monitoring and session sync.
- **Database**: PostgreSQL (Supabase) with local SQLite fallback.

---

## 🛠️ Installation & Setup

### Prerequisites
- **Node.js**: v18 or higher.
- **Python**: v3.12 or higher.
- **Git**: For version control.

### 1. Clone the Repository
```bash
git clone https://github.com/ANUPRIYA2007/ai-assessment.git
cd ai-assessment
```

### 2. Backend Setup
```bash
cd proctorforge/server
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
python main.py
```
*Backend will be running at `http://localhost:8001`*

### 3. Frontend Setup
```bash
cd proctorforge/client
npm install
npm run dev
```
*Frontend will be running at `http://localhost:3000`*

---

## 🎓 User Roles
| Role | Capabilities |
| :--- | :--- |
| **Admin** | System architecture, Class management, Direct student onboarding, Health monitoring. |
| **Teacher** | MCQ/Coding test creation, Live Proctoring, Real-time reporting, Assignment management. |
| **Student** | Exam participation, AI security validation, Result tracking, Code submission. |

---

## 🛡️ Security Policies
- **No Clipboard**: Students cannot copy or paste within the exam environment.
- **Fullscreen Enforcement**: Testing automatically ends if fullscreen is exited.
- **Device Fingerprinting**: Prevents account sharing across multiple machines.
- **AI Gaze Check**: Detects if a student is looking away from the screen for prolonged periods.

---

© 2026 ProctorForge AI. Built for the future of secure digital education.