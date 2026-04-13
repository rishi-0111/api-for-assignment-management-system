# ProctorForge AI - Deployment & Local Setup Guide

## Project Structure

The project is now separated into two independent deployable applications:

```
project/
├── frontend/          # Next.js frontend application (Deploy to Vercel)
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── .env.local     # Local development (not committed)
│   ├── .env.example   # Template for environment variables
│   └── vercel.json    # Vercel deployment configuration
│
├── backend/           # FastAPI backend application (Deploy to Railway)
│   ├── routers/       # API route handlers
│   ├── models/        # Database models
│   ├── services/      # Business logic
│   ├── main.py        # Application entry point
│   ├── requirements.txt
│   ├── .env           # Production environment variables
│   ├── .env.local     # Local development (not committed)
│   ├── .env.example   # Template for environment variables
│   ├── Dockerfile     # Container configuration
│   └── railway.json   # Railway deployment configuration
│
└── proctorforge/      # (Legacy - can be deleted)
```

## Local Development Setup

### Prerequisites

- **Node.js** 18+ and **npm** (for frontend)
- **Python** 3.10+ (for backend)
- **PostgreSQL** or **SQLite** (database)
- **Redis** (optional, for caching and WebSockets)

### 1. Setup Backend

```bash
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

# Create .env.local file (or copy from .env.example)
cp .env.example .env.local

# Edit .env.local with your local settings
# For local development, SQLite is recommended:
# DATABASE_URL=sqlite+aiosqlite:///./proctorforge.db?check_same_thread=false

# Run migrations (if applicable)
alembic upgrade head

# Start the backend server
python main.py
# Or use uvicorn directly:
# uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at: **http://localhost:8000**

### 2. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# The .env.local should point to your local backend:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Start the frontend development server
npm run dev
```

The frontend will be available at: **http://localhost:3000**

### 3. Verify Local Setup

1. **Backend Health Check**: Visit http://localhost:8000/api/health
2. **Backend Docs**: Visit http://localhost:8000/docs (SwaggerUI)
3. **Frontend App**: Visit http://localhost:3000

## Backend Deployment (Railway)

### Prerequisites

- Railway.app account (https://railway.app)
- GitHub repository with the code
- PostgreSQL database (Railway provides one)
- Optional: Redis add-on from Railway

### Deployment Steps

1. **Connect Railway to GitHub**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize and select your repository

2. **Configure Backend Service**
   - Select the `backend/` directory
   - Railway should auto-detect the Dockerfile
   - If not, manually set root directory to `backend/`

3. **Set Environment Variables in Railway**
   - Copy all variables from `backend/.env.example`
   - For Supabase PostgreSQL:
     ```
     DATABASE_URL=postgresql+asyncpg://user:password@host/database
     DATABASE_URL_SYNC=postgresql://user:password@host/database
     ```
   - For Redis: Enable Railway's Redis add-on or provide your Redis URL
   - Set `CORS_ORIGINS` to include your Vercel frontend URL:
     ```
     CORS_ORIGINS=https://your-app.vercel.app
     ```
   - Set other required variables (JWT_SECRET_KEY, ANTHROPIC_API_KEY, etc.)

4. **Deploy**
   - Railway will automatically deploy on git push
   - View logs in Railway dashboard
   - Get your backend URL from Railway (e.g., `https://your-project.railway.app`)

### Update Frontend for Production

Once backend is deployed on Railway, update `frontend/.env.production`:

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
NEXT_PUBLIC_WS_URL=wss://your-backend-url.railway.app
```

## Frontend Deployment (Vercel)

### Prerequisites

- Vercel account (https://vercel.com)
- GitHub repository with the code

### Deployment Steps

1. **Connect Vercel to GitHub**
   - Go to https://vercel.com/new
   - Click "Import Git Repository"
   - Select your repository

2. **Configure Vercel Settings**
   - **Framework**: Next.js (should be auto-detected)
   - **Root Directory**: Set to `frontend/`
   - **Build Command**: `npm run build`
   - **Start Command**: `npm start`
   - **Output Directory**: `.next`

3. **Set Environment Variables**
   - In Vercel dashboard, go to Settings → Environment Variables
   - Add:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
     NEXT_PUBLIC_WS_URL=wss://your-backend-url.railway.app
     ```

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy automatically
   - Get your frontend URL (e.g., `https://your-app.vercel.app`)

5. **Update Backend CORS**
   - Go to Railway dashboard
   - Update `CORS_ORIGINS` environment variable:
     ```
     CORS_ORIGINS=https://your-app.vercel.app
     ```

## Environment Variables Reference

### Frontend (`.env.local` or `.env.example`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000          # Backend API URL
NEXT_PUBLIC_WS_URL=ws://localhost:8000             # WebSocket URL
NEXT_PUBLIC_SUPABASE_URL=https://...               # Optional: Supabase URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=...                  # Optional: Supabase Key
```

### Backend (`.env` or `.env.example`)

```env
# Database
DATABASE_URL=postgresql+asyncpg://...              # Async database connection
DATABASE_URL_SYNC=postgresql://...                 # Sync database connection

# Authentication
JWT_SECRET_KEY=your-secret-key                     # JWT signing key
JWT_ALGORITHM=HS256                                # JWT algorithm
JWT_EXPIRATION_MINUTES=1440                        # Token expiration

# Supabase
SUPABASE_URL=https://...                           # Supabase project URL
SUPABASE_ANON_KEY=...                              # Supabase anon key
SUPABASE_SERVICE_ROLE_KEY=...                      # Supabase service role

# CORS
CORS_ORIGINS=...                                   # Comma-separated allowed origins

# Server
SERVER_HOST=0.0.0.0                                # Bind to all interfaces
SERVER_PORT=8000                                   # Server port
```

## Troubleshooting

### Backend won't start

1. **Check Python version**: `python --version` (should be 3.10+)
2. **Verify virtual environment**: Source/activate the venv
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Check database connection**: Verify DATABASE_URL in .env.local
5. **Check logs**: Look for error messages

### Frontend can't connect to backend

1. **Check CORS**: Backend's `CORS_ORIGINS` must include frontend URL
2. **Check API URL**: `NEXT_PUBLIC_API_URL` must be correct
3. **Network**: Ensure backend is running and accessible
4. **Browser console**: Check for network errors

### WebSocket connection failed

1. **Check WebSocket URL**: `NEXT_PUBLIC_WS_URL` should match backend URL
2. **Backend logs**: Check for WebSocket errors
3. **Firewall**: Ensure port 8000 is not blocked

### Railway Deployment Issues

1. **Dockerfile errors**: Ensure Dockerfile is in `backend/` directory
2. **Dependencies**: All requirements in `requirements.txt` must install
3. **Logs**: Check Railway deployment logs for errors
4. **Environment variables**: All required variables must be set

### Vercel Deployment Issues

1. **Root directory**: Ensure `frontend/` is set as root directory
2. **Build errors**: `npm run build` should work locally first
3. **Environment variables**: Must be set in Vercel settings
4. **API connectivity**: Frontend must be able to reach backend

## CI/CD Pipeline

Both services can be configured for automatic deployment:

- **Backend**: Push to main branch → Railway auto-deploys
- **Frontend**: Push to main branch → Vercel auto-deploys

No additional CI/CD configuration needed if using Railway and Vercel directly.

## Production Checklist

- [ ] Set strong JWT_SECRET_KEY and HMAC_SECRET_KEY
- [ ] Use PostgreSQL (not SQLite) in production
- [ ] Set CORS_ORIGINS to specific domains (not *)
- [ ] Enable HTTPS/WSS in production
- [ ] Set up monitoring and logging
- [ ] Configure backups for database
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Test all authentication flows
- [ ] Load test before launch
- [ ] Have a rollback plan

## Support

For issues or questions:
- Check logs in Railway/Vercel dashboards
- Review backend API docs at `/docs`
- Check Network tab in browser dev tools
