# ProctorForge AI - Quick Reference Card

## Project Structure
```
project/
├── frontend/          → Next.js app (Deploy to Vercel)
├── backend/           → FastAPI app (Deploy to Railway)
├── DEPLOYMENT_GUIDE.md
└── LOCAL_SETUP.md
```

## Local Development (5 min setup)

### Terminal 1 - Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
# Visit: http://localhost:8000/docs
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
# Visit: http://localhost:3000
```

## Environment Variables

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Backend (`.env.local`)
```env
DATABASE_URL=sqlite+aiosqlite:///./proctorforge.db?check_same_thread=false
JWT_SECRET_KEY=dev-key
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Deployment Commands

### Deploy Backend to Railway
```bash
# 1. Go to https://railway.app
# 2. Click "New Project" → "Deploy from GitHub repo"
# 3. Select repo, set root to backend/
# 4. Add environment variables from backend/.env.example
# 5. Deploy!
```

### Deploy Frontend to Vercel
```bash
# 1. Go to https://vercel.com/new
# 2. Import GitHub repo
# 3. Set root to frontend/
# 4. Add NEXT_PUBLIC_API_URL pointing to Railway
# 5. Deploy!
```

## Common Commands

### Backend
```bash
cd backend
python main.py                    # Run server
python -m pytest                  # Run tests
alembic upgrade head             # Run migrations
curl http://localhost:8000/docs  # View API docs
```

### Frontend
```bash
cd frontend
npm run dev          # Development server
npm run build        # Production build
npm run start        # Run production build locally
npm run lint         # Check code
npm run lint:fix     # Fix errors
```

### Docker
```bash
docker-compose up -d        # Start all services
docker-compose down         # Stop all services
docker-compose logs -f      # View logs
docker-compose ps           # List running services
```

## Verify Setup

- [ ] Backend at http://localhost:8000/api/health
- [ ] Frontend at http://localhost:3000
- [ ] API docs at http://localhost:8000/docs
- [ ] No CORS errors in browser console

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Use different port: `python main.py --port 8001` |
| Port 3000 in use | Use different port: `npm run dev -- -p 3001` |
| CORS error | Check `CORS_ORIGINS` in backend `.env` |
| Database error | Delete `.db` file and restart backend |
| Cannot connect | Verify backend is running: `curl http://localhost:8000/api/health` |

## File Reference

| File | Purpose |
|------|---------|
| DEPLOYMENT_GUIDE.md | Complete deployment & setup guide |
| LOCAL_SETUP.md | Step-by-step local development guide |
| backend/.env.example | Backend env template |
| frontend/.env.example | Frontend env template |
| docker-compose.yml | Containerized local setup |
| Vercel.json | Vercel deployment config |
| railway.json | Railway deployment config |

## Architecture

```
┌─────────────────────────────────────────┐
│         Vercel (Frontend)               │
│  http://app.vercel.app                  │
│  - Next.js 16                           │
│  - React 19                             │
│  - Tailwind CSS                         │
└──────────────┬──────────────────────────┘
               │
               │ HTTP/WebSocket
               │ API Calls
               │
┌──────────────▼──────────────────────────┐
│        Railway (Backend)                │
│  https://backend.railway.app            │
│  - FastAPI                              │
│  - PostgreSQL                           │
│  - Redis                                │
└─────────────────────────────────────────┘
```

## Important URLs

| Service | Local | Production |
|---------|-------|------------|
| Frontend | http://localhost:3000 | https://app.vercel.app |
| Backend API | http://localhost:8000 | https://backend.railway.app |
| API Docs | http://localhost:8000/docs | https://backend.railway.app/docs |
| WebSocket | ws://localhost:8000 | wss://backend.railway.app |

## Git Workflow

```bash
# Make changes
git add .
git commit -m "Your message"
git push origin main

# Railway auto-deploys backend/
# Vercel auto-deploys frontend/
```

## Support Resources

- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Full setup & deployment
- [LOCAL_SETUP.md](./LOCAL_SETUP.md) - Local development details
- [README.md](./README.md) - Project overview
- Backend Docs: http://localhost:8000/docs (when running)
- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs

---

**Last Updated**: April 2026
