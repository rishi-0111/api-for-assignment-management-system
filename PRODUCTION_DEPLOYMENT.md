# ProctorForge AI - Production Deployment Guide
## Vercel + Railway Complete Setup

This guide provides step-by-step instructions to deploy your separated full-stack application to production using Vercel for the frontend and Railway for the backend.

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   VERCEL FRONTEND                   │
│  https://your-app.vercel.app                        │
│  ├─ UI Components (React/Next.js)                  │
│  ├─ Pages (Login, Dashboard, Exams, etc.)          │
│  ├─ Stores (Zustand for state management)          │
│  └─ API Calls (Axios to Railway backend)           │
└────────────────────┬────────────────────────────────┘
                     │
          HTTPS/WebSocket API Calls
                     │
┌────────────────────▼────────────────────────────────┐
│                  RAILWAY BACKEND                    │
│  https://your-backend.railway.app                   │
│  ├─ FastAPI Server (Port 8000)                     │
│  ├─ API Endpoints (/api/auth, /api/exams, etc.)   │
│  ├─ Database (PostgreSQL)                          │
│  ├─ Cache (Redis)                                  │
│  └─ Business Logic & Authentication                │
└─────────────────────────────────────────────────────┘
```

---

## 📋 Pre-Deployment Checklist

### Local Verification
- [ ] Backend runs locally: `python backend/main.py`
- [ ] Frontend runs locally: `npm run dev`
- [ ] Frontend connects to backend API
- [ ] No console errors
- [ ] Login/Register works
- [ ] Dashboard loads
- [ ] API calls work properly

### Code Quality
- [ ] No hardcoded URLs (using environment variables)
- [ ] All database operations through APIs
- [ ] CORS configured
- [ ] JWT authentication implemented
- [ ] Error handling in place

### Environment Variables
- [ ] `.env.example` files updated
- [ ] `.env` files NOT committed to git
- [ ] Supabase/PostgreSQL credentials available
- [ ] Secret keys generated

---

## 🚀 Step 1: Deploy Backend to Railway

### Step 1.1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (easiest option)
3. Authorize Railway to access your GitHub account

### Step 1.2: Create a New Railway Project
1. Click **"New Project"**
2. Click **"Deploy from GitHub Repo"**
3. Select your GitHub repository (rishi-0111/api-for-assignment-management-system)
4. Click **"Next"**

### Step 1.3: Configure Root Directory
1. In the deploy configuration page:
   - **Root Directory**: Set to `backend/`
   - **Branch**: `main`
2. Click **"Next"**

### Step 1.4: Add Environment Variables

Railway will auto-deploy, but first add environment variables:

1. Go to your Railway project dashboard
2. Click on the **backend** service
3. Go to **Variables** tab
4. Add  environment variables from your `.env.example`:

```env
# ===== DATABASE =====
# Use Railway's PostgreSQL plugin for production
DATABASE_URL=postgresql+asyncpg://user:password@your-railway-db-host:5432/proctorforge
DATABASE_URL_SYNC=postgresql://user:password@your-railway-db-host:5432/proctorforge

# ===== JWT SECURITY =====
JWT_SECRET_KEY=<generate-new-secure-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# ===== HMAC SECURITY =====
HMAC_SECRET_KEY=<generate-new-secure-key>

# ===== SUPABASE =====
SUPABASE_URL=https://tubwqpzbmoqvfwnlhcql.supabase.co
SUPABASE_ANON_KEY=<your-supabase-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-supabase-service-role-key>

# ===== REDIS ===== 
# Railway will provide this after adding the Redis plugin
REDIS_URL=redis://:<password>@<host>:<port>

# ===== SERVER =====
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# ===== CORS ===== 
# Start with local, will update after Vercel deployment
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# ===== LOGGING =====
LOG_LEVEL=info

# ===== AI FEATURES =====
ANTHROPIC_API_KEY=<your-key-if-using>
```

### Step 1.5: Add Database (PostgreSQL)
1. In Railway dashboard, click **"+ Add"**
2. Select **"PostgreSQL"**
3. This will automatically add `DATABASE_URL` environment variable
4. Wait for the database to be provisioned

### Step 1.6: Add Cache (Redis)
1. Click **"+ Add"** again
2. Select **"Redis"**
3. This will automatically add `REDIS_URL` environment variable

### Step 1.7: Trigger Deployment
1. Railway auto-deploys after adding environment variables
2. Wait for logs to show: `✅ Database tables created` and `Uvicorn running on`
3. Get your Railway backend URL from the Dashboard (looks like: `https://projectname-production.up.railway.app`)

### Step 1.8: Test Backend
```bash
# Test health check
curl https://your-railway-backend-url/api/health

# Should return:
# {"status":"healthy","service":"proctorforge-backend"}

# View API documentation
# Visit: https://your-railway-backend-url/docs
```

### Step 1.9: Generate Secure Keys

Before updating CORS, generate strong secret keys:

```bash
# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate HMAC_SECRET_KEY  
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update these in Railway's environment variables.

---

## 🌐 Step 2: Deploy Frontend to Vercel

### Step 2.1: Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub (easiest option)
3. Authorize Vercel to access your GitHub account

### Step 2.2: Import Project
1. Click **"Add New"** → **"Project"**
2. Click **"Import Git Repository"**
3. Search for: `rishi-0111/api-for-assignment-management-system`
4. Click **"Import"**

### Step 2.3: Configure for Monorepo
1. In the project settings:
   - **Project Name**: Give it a name (e.g., "proctorforge-ai")
   - **Framework**: Next.js (should be auto-detected)
   - **Root Directory**: Set to `frontend/`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

### Step 2.4: Add Environment Variables (CRITICAL!)
1. Click on **"Environment Variables"** tab
2. Add the following:

```env
NEXT_PUBLIC_API_URL=https://your-railway-backend-url
NEXT_PUBLIC_WS_URL=wss://your-railway-backend-url
```

**Important**: 
- Use `https://` for HTTP API calls
- Use `wss://` for WebSocket connections  
- Replace `your-railway-backend-url` with your actual Railway URL (from Step 1.7)

### Step 2.5: Deploy
1. Click **"Deploy"**
2. Wait for build to complete (usually 2-3 minutes)
3. Get your Vercel frontend URL (looks like: `https://proctorforge-ai.vercel.app`)

### Step 2.6: Test Frontend
1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Check browser console (F12) for any errors
3. Check Network tab - API calls should go to your Railway backend

---

## 🔗 Step 3: Connect Frontend & Backend

### Step 3.1: Update Backend CORS

Now that Vercel frontend is deployed, update the backend's CORS settings:

1. Go to Railway dashboard
2. Go to backend service → Variables
3. Update `CORS_ORIGINS`:

```env
CORS_ORIGINS=https://your-app.vercel.app
```

4. Railway will auto-redeploy

### Step 3.2: Test Connection

1. Go to your Vercel app
2. Open browser DevTools (F12)
3. Go to Network tab
4. Try any action (login, Create exam, etc.)
5. You should see API calls to your Railway backend
6. All should return 200/201 status

### Step 3.3: Test Specific Flows

**Login Flow:**
1. Go to login page
2. Enter credentials
3. Check Network tab → POST to `/api/auth/login`
4. Should return JWT token
5. Check localStorage → `proctorforge_token` should exist

**Dashboard:**
1. After login, go to dashboard
2. Check Network tab → GET to `/api/exams` (or similar)
3. Data should load from Railway backend

**WebSocket (if applicable):**
1. Open DevTools → Console
2. Run: `new WebSocket('wss://your-backend-url/ws/...')`
3. Should connect successfully (no `Connection refused` error)

---

## 🔐 Environment Variables Reference

### Frontend (Set in Vercel)
```env
# API Endpoint
NEXT_PUBLIC_API_URL=https://your-backend.railway.app

# WebSocket Endpoint
NEXT_PUBLIC_WS_URL=wss://your-backend.railway.app

# Optional: Analytics
NEXT_PUBLIC_GA_ID=optional-google-analytics-id

# Optional: Supabase Direct Access
# Only if frontend accesses Supabase directly
# NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
# NEXT_PUBLIC_SUPABASE_ANON_KEY=your-key
```

### Backend (Set in Railway)
```env
# Database
DATABASE_URL=postgresql+asyncpg://...
DATABASE_URL_SYNC=postgresql://...

# Authentication
JWT_SECRET_KEY=strong-random-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# HMAC
HMAC_SECRET_KEY=strong-random-key

# Supabase
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...

# Redis
REDIS_URL=redis://...

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# CORS - Include your Vercel frontend URL
CORS_ORIGINS=https://your-app.vercel.app

# Logging
LOG_LEVEL=info

# AI Features (if used)
ANTHROPIC_API_KEY=...
```

---

## 📊 Data Flow Architecture

### How Frontend → Backend Communication Works

```
┌─ Vercel Frontend ─────────────────────────────────────────┐
│  1. User clicks "Login"                                   │
│  2. Frontend sends HTTP POST to:                          │
│     https://your-backend.railway.app/api/auth/login       │
│  3. Vercel sends HTTPS request to Railway                │
│  4. Railway backend authenticates user                    │
│  5. Backend queries PostgreSQL database                   │
│  6. Backend generates JWT token                           │
│  7. Backend returns token to Vercel                       │
│  8. Frontend stores token in localStorage                 │
│  9. All future requests include Authorization header      │
│  10. CORS allows this cross-domain communication         │
└──────────────────────────────────────────────────────────┘
```

### Database Operations Flow

```
Frontend (Vercel)
      │
      │ API Call (e.g., GET /api/exams)
      ▼
Railway Backend
      │
      │ SQL Query
      ▼
PostgreSQL Database (Railway)
      │
      │ Return Data
      ▼
Railway Backend
      │
      │ Return JSON Response
      ▼
Frontend (Vercel)
      │
      │ Parse & Display to User
      ▼
User Browser
```

### Authentication Flows

**Login Flow:**
```
1. Frontend: POST /api/auth/login { email, password }
2. Backend: Hash password, check database
3. Backend: Generate JWT token
4. Backend: Return { token, user }
5. Frontend: Store token in localStorage
6. Frontend: Attach token to all future requests
```

**Protected Endpoints:**
```
1. Frontend: GET /api/exams
   Headers: { "Authorization": "Bearer <token>" }
2. Backend: Verify JWT token from header
3. Backend: If valid, return data
4. Backend: If invalid, return 401 Unauthorized
5. Frontend: Intercept 401, redirect to login
```

---

## 🧪 Complete Testing Checklist

### After Deployment
- [ ] Backend health check works: `/api/health` → 200
- [ ] Backend API docs accessible: `/docs`
- [ ] Frontend loads without errors
- [ ] No Network errors in browser console
- [ ] CORS not blocking requests
- [ ] JWT tokens being created/stored

### Authentication
- [ ] Can register new user ✓
- [ ] Can login with credentials ✓
- [ ] Token stored in localStorage ✓
- [ ] Token sent in Authorization header ✓
- [ ] Logout clears token ✓
- [ ] 401 redirects to login ✓

### Features
- [ ] Dashboard loads ✓
- [ ] Create exam works ✓
- [ ] View exams works ✓
- [ ] Edit exam works ✓
- [ ] Delete exam works ✓
- [ ] Join exam works ✓
- [ ] Submit exam works ✓
- [ ] Analytics displays data ✓

### Database
- [ ] Users created correctly ✓
- [ ] Exams saved correctly ✓
- [ ] Attempts recorded correctly ✓
- [ ] Data persists after refresh ✓

### Performance
- [ ] API responses < 500ms ✓
- [ ] Frontend loads < 3 seconds ✓
- [ ] No Vercel function timeouts ✓
- [ ] No Railway service crashes ✓

---

## 🔧 Troubleshooting

### Frontend Can't Connect to Backend

**Error**: Network Error / Failed to fetch / CORS Error

**Solutions**:
1. **Check API URL**: Open DevTools → Console
   ```javascript
   console.log(process.env.NEXT_PUBLIC_API_URL)
   ```
   Should show your Railway URL

2. **Check CORS**: Backend must include frontend URL
   - Go to Railway dashboard
   - Check `CORS_ORIGINS` environment variable
   - Must include your Vercel frontend URL

3. **Check if backend is running**:
   ```bash
   curl https://your-backend-url/api/health
   ```

4. **Check network tab**: F12 → Network
   - Look for failed API requests
   - Check status code
   - Read response body for error message

### 401 Unauthorized Errors

**Problem**: Getting 401 on protected endpoints

**Solutions**:
1. Ensure token is being sent:
   ```javascript
   // Check if token exists
   console.log(localStorage.getItem('proctorforge_token'))
   ```

2. Check if token is valid:
   - Decode token at https://jwt.io
   - Check expiration time
   - Check if it was generated by backend

3. Backend might be restarted:
   - Check Railway logs
   - Look for crashes or errors
   - Restart backend service if needed

### Database Connection Errors

**Problem**: Backend can't connect to database

**Solutions**:
1. Check DATABASE_URL is correct:
   - Go to Railway
   - Check PostgreSQL service settings
   - Copy correct connection string

2. Verify credentials:
   - Username correct
   - Password correct
   - Database name correct

3. Check network connectivity:
   - Railway PostgreSQL should be accessible from backend
   - May need IP whitelist
   - May need SSL certificate

### WebSocket Connection Failed

**Problem**: WebSocket can't connect

**Solutions**:
1. Check WebSocket URL:
   ```env
   NEXT_PUBLIC_WS_URL=wss://your-backend-url
   ```
   - Use `wss://` not `ws://`
   - Must use HTTPS domain

2. Check backend logs in Railway:
   - Look for WebSocket connection logs
   - Check for any errors

3. Railway might not support WebSocket:
   - Some deployment platforms block WebSocket
   - May need different configuration

---

## 🚨 Production Best Practices

### Security
1. ✅ Never commit `.env` files  
2. ✅ Use strong JWT_SECRET_KEY (generate new for production)
3. ✅ Use HTTPS only (Vercel & Railway provide SSL)
4. ✅ Set specific CORS_ORIGINS (not `*`)
5. ✅ Validate all inputs on backend
6. ✅ Use HTTPS for database connections
7. ✅ Enable database backups

### Monitoring
1. ✅ Setup error tracking (Sentry, LogRocket, etc.)
2. ✅ Monitor Railway logs for errors
3. ✅ Monitor Vercel performance
4. ✅ Set up alerting for failures
5. ✅ Track API response times

### Performance
1. ✅ Enable database query caching
2. ✅ Use Redis for session caching
3. ✅ Implement API rate limiting
4. ✅ Use CDN for static assets
5. ✅ Optimize database queries
6. ✅ Enable compression on REST API

### Maintenance
1. ✅ Regular database backups
2. ✅ Monitor disk usage
3. ✅ Keep dependencies updated
4. ✅ Roll out updates gradually
5. ✅ Have rollback plan

---

## 📈 Scaling Tips

### When Frontend Needs More Power
- Vercel automatically scales per region
- No action needed for typical usage
- Pro plan for higher limits

### When Backend Needs More Power
1. Upgrade Railway plan
2. Add more Railway services (load balancing)
3. Optimize database queries
4. Use caching more aggressively

### When Database Needs More Power
1. Upgrade PostgreSQL plan on Railway
2. Add read replicas
3. Implement database sharding
4. Archive old data periodically

---

## 🎯 Next Steps After Deployment

1. **Monitor**: Check logs daily for first week
2. **Test**: Run full testing suite weekly
3. **Optimize**: Profile slow API endpoints
4. **Update**: Deploy bug fixes as needed
5. **Improve**: Add new features based on feedback
6. **Secure**: Review security monthly

---

## 🆘 Get Help

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Next.js Docs**: https://nextjs.org/docs
- **GitHub Issues**: Check your repository

---

**Deployment Complete! Your app is now live on the internet! 🎉**
