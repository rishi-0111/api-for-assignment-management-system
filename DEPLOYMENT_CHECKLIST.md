# ✅ ProctorForge AI - Deployment Checklist

## Phase 1: Pre-Deployment Verification ✓

### Code Separation
- [x] Frontend separated into `/frontend` directory
- [x] Backend separated into `/backend` directory  
- [x] Unnecessary files removed from each
- [x] Import paths corrected

### Frontend Setup
- [x] `frontend/src/lib/api.ts` configured for backend API
- [x] `frontend/.env.example` created with all needed variables
- [x] `frontend/.env.local` created for local development
- [x] `frontend/vercel.json` added for Vercel deployment
- [x] All API calls go through axios client (no direct DB access)
- [x] Authentication tokens stored in localStorage
- [x] Request interceptors add JWT tokens to headers
- [x] Response interceptors handle 401 errors

### Backend Setup
- [x] `backend/main.py` contains proper FastAPI application
- [x] All routers imported: auth, exams, attempts, websocket, code_execution, monitoring
- [x] CORS middleware configured in `backend/main.py`
- [x] `backend/config.py` loads environment variables correctly
- [x] `backend/.env.example` created with all needed variables
- [x] `backend/.env.local` created for local development
- [x] `backend/railway.json` added for Railway deployment
- [x] All database operations through API routes
- [x] Error handling implemented
- [x] Logging configured

### Environment Variables
- [x] All hardcoded URLs removed
- [x] Environment variables used throughout
- [x] `.env.example` templates created for reference
- [x] `.env.local` files configured for local dev
- [x] Production `.env` template documented

### Documentation
- [x] README.md - Main entry point and overview
- [x] PRODUCTION_DEPLOYMENT.md - Step-by-step deployment guide (300+ lines)
- [x] FRONTEND_BACKEND_INTEGRATION.md - Architecture and communication (400+ lines)
- [x] TERMINAL_DEPLOYMENT_GUIDE.md - All CLI commands (300+ lines)
- [x] LOCAL_SETUP.md - Local development guide
- [x] QUICK_REFERENCE.md - Quick command reference
- [x] PROJECT_COMPLETION_SUMMARY.md - Summary of changes
- [x] DEPLOYMENT_CHECKLIST.md - This checklist

### Git & Version Control
- [x] All changes staged with `git add -A`
- [x] Changes committed with descriptive message
- [x] Changes pushed to GitHub
- [x] Commits visible in GitHub repo
- [x] No uncommitted changes

---

## Phase 2: Local Testing (Do This Now)

### Backend Local Test
- [ ] Terminal 1: `cd backend`
- [ ] Terminal 1: Create venv: `python -m venv venv`
- [ ] Terminal 1: Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
- [ ] Terminal 1: Install deps: `pip install -r requirements.txt`
- [ ] Terminal 1: Run backend: `python main.py`
- [ ] Expected: FastAPI running at http://localhost:8000
- [ ] Verify: Open http://localhost:8000/docs → API docs load
- [ ] Verify: GET http://localhost:8000/api/health → Returns {"status": "healthy", "service": "proctorforge-backend"}

### Frontend Local Test
- [ ] Terminal 2: `cd frontend`
- [ ] Terminal 2: `npm install` (first time only)
- [ ] Terminal 2: `npm run dev`
- [ ] Expected: Next.js running at http://localhost:3000
- [ ] Verify: Browser opens http://localhost:3000 → Loads without errors
- [ ] Verify: Browser console → No errors or warnings about API
- [ ] Verify: Network tab → Frontend can connect to backend

### End-to-End Local Test
- [ ] Navigate to http://localhost:3000
- [ ] Click "Register" or "Login"
- [ ] Enter test credentials
- [ ] Network tab shows: POST /api/auth/register or /api/auth/login
- [ ] Status code: 201 or 200 (not 404 or 500)
- [ ] Response contains JWT token
- [ ] Redirects to dashboard
- [ ] Dashboard loads data from backend
- [ ] All features work (create, read, update, delete if applicable)

---

## Phase 3: Production Deployment

### Prepare Repository
- [ ] No `.env` files with secrets committed (should be .env.local or .env.example)
- [ ] No hardcoded API URLs (all use env variables)
- [ ] No console.log debug statements
- [ ] No commented-out code chunks
- [ ] Package.json versions are correct
- [ ] requirements.txt is up to date

### Deploy Backend to Railway

**Step 1: Create Railway Account**
- [ ] Go to https://railway.app
- [ ] Sign up with GitHub (easier)
- [ ] Link your GitHub account

**Step 2: Deploy Backend Project**
- [ ] Click "New Project" (or + button)
- [ ] Select "Deploy from GitHub repo"
- [ ] Select your repository
- [ ] Select `backend` as the root directory
- [ ] Click "Deploy"

**Step 3: Add Environment Variables**
- [ ] In Railway dashboard, go to Variables
- [ ] Add each variable from `backend/.env.example`:
  - `DATABASE_URL` - Supabase PostgreSQL connection URL
  - `JWT_SECRET_KEY` - Generate strong random key (32+ chars)
  - `HMAC_SECRET_KEY` - Generate strong random key (32+ chars)
  - `SUPABASE_URL` - From Supabase project
  - `SUPABASE_ANON_KEY` - From Supabase project
  - `SUPABASE_SERVICE_ROLE_KEY` - From Supabase project (keep secret!)
  - `REDIS_URL` - Optional (add Redis addon if needed)
  - `CORS_ORIGINS` - Leave as `http://localhost:3000` for now
  - `SERVER_PORT` - Should be `8000`
  - `SERVER_HOST` - Should be `0.0.0.0`
- [ ] Click "Save Variables"

**Step 4: Add Database Addon**
- [ ] In Railway dashboard, click "Add Service"
- [ ] Search "PostgreSQL"
- [ ] Click "PostgreSQL" at the top
- [ ] Click "Add"
- [ ] Wait for database to initialize (2-3 minutes)
- [ ] Copy DATABASE_URL from PostgreSQL service variables
- [ ] Paste into backend's DATABASE_URL environment variable
- [ ] Re-deploy backend

**Step 5: Verify Deployment**
- [ ] Wait for deployment status to show "Running" (green)
- [ ] Click deployment to see URL
- [ ] Test endpoint: `curl https://your-railway-url.railway.app/api/health`
- [ ] Should return: `{"status": "healthy", "service": "proctorforge-backend"}`
- [ ] Backend is live! ✓

**Step 6: Get Backend URL**
- [ ] Copy your Railway backend URL (remove trailing slash)
- [ ] Example: `https://proctorforge-backend-prod.railway.app`
- [ ] Save this for next steps

### Deploy Frontend to Vercel

**Step 1: Create Vercel Account**
- [ ] Go to https://vercel.com
- [ ] Sign up with GitHub (easier)
- [ ] Link your GitHub account

**Step 2: Import Project**
- [ ] Click "Add New" button
- [ ] Select "Project"
- [ ] Click "Import Git Repository"
- [ ] Find and select your GitHub repository
- [ ] Click "Import"

**Step 3: Configure Settings**
- [ ] Framework: Should auto-detect "Next.js" ✓
- [ ] Root Directory: Change to `frontend/`
- [ ] Build Command: Should be auto-detected
- [ ] Output Directory: Should be auto-detected

**Step 4: Add Environment Variables**
- [ ] In Vercel settings, click "Environment Variables"
- [ ] Add these variables (Production):
  - `NEXT_PUBLIC_API_URL` = `https://your-railway-url.railway.app` (from step 6 above)
  - `NEXT_PUBLIC_WS_URL` = `wss://your-railway-url.railway.app` (replace http with ws)
- [ ] Make sure they're set for "Production" environment
- [ ] Click "Save"

**Step 5: Deploy**
- [ ] Click "Deploy" button
- [ ] Wait for deployment to complete (3-5 minutes)
- [ ] You'll see "Congratulations! Your site is ready"
- [ ] Copy your Vercel URL (example: `https://proctorforge.vercel.app`)

**Step 6: Verify Frontend Deployment**
- [ ] Open your Vercel URL in browser
- [ ] Page should load (may take 10-20 seconds first time)
- [ ] No errors in browser console
- [ ] Try to login/register
- [ ] Should connect to your Railway backend

### Connect Frontend & Backend

**Update CORS on Backend**
- [ ] Go to Railway dashboard, select your backend project
- [ ] Go to Variables
- [ ] Update `CORS_ORIGINS` with your Vercel URL:
  ```
  http://localhost:3000,https://your-vercel-url.vercel.app
  ```
- [ ] Save
- [ ] Deployment will auto-redeploy with new CORS settings

**Wait for redeployment**
- [ ] Check deployment status in Railway (should go to "Running" again)
- [ ] Takes about 2-3 minutes

### Final End-to-End Test

**Test 1: Frontend Loads**
- [ ] Open `https://your-vercel-url.vercel.app`
- [ ] Page loads without errors
- [ ] No "API not found" or "CORS" errors

**Test 2: Authentication Works**
- [ ] Click "Register" 
- [ ] Fill in form with test data
- [ ] Submit
- [ ] Should see success or redirect to login
- [ ] Network tab: POST /api/auth/register status 201 or 200

**Test 3: Data Operations**
- [ ] Login with test account
- [ ] Go to relevant section (exams, analytics, etc.)
- [ ] Create/Read/Update/Delete operations
- [ ] All should work without errors
- [ ] Network tab: All API requests return 2xx status

**Test 4: Real-Time (if applicable)**
- [ ] Test WebSocket connections
- [ ] Real-time updates should work
- [ ] Network tab: WS connection shows "101 Switching Protocols"

---

## Phase 4: Post-Deployment

### Monitoring
- [ ] Set up Railway monitoring/alerts (optional)
- [ ] Set up Vercel monitoring/alerts (optional)
- [ ] Check logs occasionally for errors

### Performance
- [ ] Test from different locations (use tools like Speedtest CLI)
- [ ] Monitor response times
- [ ] Optimize if needed

### Security
- [ ] Verify HTTPS is used (should be automatic)
- [ ] Verify JWT tokens are not exposed in URLs
- [ ] Verify sensitive data is not logged
- [ ] Review environment variables are correct

### Backups
- [ ] Verify database backups are configured (Railway PostgreSQL)
- [ ] Test restore process
- [ ] Document backup procedure

### Documentation Updates
- [ ] Update any docs with production URLs
- [ ] Document any custom configurations
- [ ] Create runbook for common issues

---

## Phase 5: Troubleshooting

### If Frontend Can't Connect to Backend
- [ ] Check `NEXT_PUBLIC_API_URL` matches Railway URL
- [ ] Check `CORS_ORIGINS` on Railway backend includes Vercel URL
- [ ] Check network tab for 403 CORS errors
- [ ] Check Railway deployment logs
- [ ] Verify Railway backend is running (check status in dashboard)

### If Deployment Fails
- [ ] Check Railway build logs for errors
- [ ] Verify all environment variables are set
- [ ] Verify DATABASE_URL is correct
- [ ] Verify root directory is correct (backend/ not proctorforge/server/)
- [ ] Check git repository for uncommitted changes

### If Backend Returns 500 Errors
- [ ] Check Railway logs for Python exceptions
- [ ] Verify database connection is working
- [ ] Verify all environment variables are set
- [ ] Check if migrations have run
- [ ] Restart the deployment

### If Frontend is Slow
- [ ] Check Vercel performance tab
- [ ] Verify backend API is responding quickly
- [ ] Check if backend is at query limits
- [ ] Consider adding caching

---

## Success Criteria ✓

Your deployment is successful when:

- ✅ Frontend loads from Vercel URL without errors
- ✅ Backend responds to API calls from Railway URL
- ✅ Frontend can register/login through backend API
- ✅ All features work end-to-end
- ✅ No CORS errors in browser console
- ✅ No connection timeout errors
- ✅ Data persists across page refreshes
- ✅ Real-time features work (if applicable)
- ✅ Logs show no errors or exceptions
- ✅ Analytics/monitoring shows healthy status

---

## Quick Reference Links

- **Railroad Documentation**: https://docs.railway.app
- **Vercel Documentation**: https://vercel.com/docs
- **Supabase Documentation**: https://supabase.io/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Next.js Documentation**: https://nextjs.org/docs

---

## Support Resources

If you get stuck:

1. **Read [PRODUCTION_DEPLOYMENT.md](./PRODUCTION_DEPLOYMENT.md)** - Detailed step-by-step guide
2. **Read [TERMINAL_DEPLOYMENT_GUIDE.md](./TERMINAL_DEPLOYMENT_GUIDE.md)** - All CLI commands
3. **Read [FRONTEND_BACKEND_INTEGRATION.md](./FRONTEND_BACKEND_INTEGRATION.md)** - How things connect
4. **Check logs** - Railway and Vercel both show detailed build/runtime logs
5. **Check CommonIssues.md** - (if exists) for known problems

---

**Status**: 🟢 Ready to Deploy

All preparation is complete. You can now follow the deployment steps above.

**Estimated time to production**: 20-30 minutes

Good luck! 🚀
