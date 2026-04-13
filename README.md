# ProctorForge AI - Full Stack Proctoring Platform

> Secure, AI-native zero-trust remote assessment platform with advanced proctoring capabilities

## 🚀 Project Overview

ProctorForge AI is now available as a **separated, deployable monorepo** with independent frontend and backend applications optimized for cloud deployment.

### Project Structure

```
project/
├── frontend/              # Next.js application → Deploy to Vercel
│   ├── src/
│   ├── package.json
│   ├── vercel.json
│   ├── .env.example
│   └── README.md
│
├── backend/               # FastAPI application → Deploy to Railway
│   ├── routers/
│   ├── models/
│   ├── services/
│   ├── main.py
│   ├── requirements.txt
│   ├── railway.json
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
│
└── DEPLOYMENT_GUIDE.md    # Complete setup & deployment guide
```

## ⚡ Quick Start

### Local Development (5 minutes)

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```
Backend runs at: **http://localhost:8000**

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: **http://localhost:3000**

### Production Deployment

#### Deploy Backend to Railway (2 minutes)
1. Login to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select repository, point to `backend/` folder
4. Add env vars from `backend/.env.example`
5. Deploy! Backend auto-deploys on git push

#### Deploy Frontend to Vercel (2 minutes)
1. Login to https://vercel.com
2. Click "Add New" → "Project"
3. Import GitHub repo, set root to `frontend/`
4. Add `NEXT_PUBLIC_API_URL` pointing to Railway backend
5. Deploy! Frontend auto-deploys on git push

## 🎯 Key Features

### Frontend (Next.js)
- ✅ Real-time exam monitoring dashboard
- ✅ AI Twin visualization
- ✅ Live student performance analytics
- ✅ Exam builder (MCQ & Coding)
- ✅ Responsive design with Tailwind CSS
- ✅ WebSocket real-time updates

### Backend (FastAPI)
- ✅ REST API for all exam operations
- ✅ WebSocket for live sessions
- ✅ JWT authentication & authorization
- ✅ Database abstraction (PostgreSQL/SQLite)
- ✅ Docker containerization
- ✅ Comprehensive test suite

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS |
| **Backend** | FastAPI, SQLAlchemy, PostgreSQL/SQLite |
| **Auth** | JWT with Supabase |
| **Real-time** | WebSocket, Socket.io |
| **Deployment** | Vercel (Frontend), Railway (Backend) |
| **Database** | PostgreSQL (production), SQLite (local) |

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Complete deployment & setup instructions
- **[backend/README.md](./backend/README.md)** - Backend documentation
- **[frontend/README.md](./frontend/README.md)** - Frontend documentation
- **API Docs** (when running locally): http://localhost:8000/docs

## 🌐 Environment Variables

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Backend (`.env.local` for development, `.env` for production)
```env
DATABASE_URL=sqlite+aiosqlite:///./proctorforge.db?check_same_thread=false
JWT_SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

See `backend/.env.example` and `frontend/.env.example` for all variables.

## 🔐 Security Features

- **Zero-Trust Architecture**: Every request authenticated
- **JWT Authentication**: Secure token-based auth
- **CORS Protection**: Configurable for production domains
- **HMAC Signing**: Event integrity verification
- **Rate Limiting**: Built-in protection
- **Encrypted Connections**: HTTPS/WSS in production

## 📦 Monorepo Structure

This is a **monorepo** where:
- `/frontend` - Next.js app (can be deployed independently)
- `/backend` - FastAPI app (can be deployed independently)
- Each has its own dependencies, environment config, and deployment setup
- Both can be developed and deployed separately

## 🚀 Deployment Pipeline

Both services support CI/CD through Git:

1. **Push to main branch**
2. **Railway watches backend/** → Auto-deploys to Railway
3. **Vercel watches frontend/** → Auto-deploys to Vercel

No additional CI/CD setup needed!

## 📋 Production Checklist

Before deploying to production:
- [ ] Update JWT secrets (generate new strong keys)
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set specific CORS origins
- [ ] Enable HTTPS certificate
- [ ] Configure database backups
- [ ] Set up monitoring and alerts
- [ ] Load test your deployment
- [ ] Have a rollback plan

## 🐛 Troubleshooting

**Frontend can't connect to backend?**
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Ensure backend `CORS_ORIGINS` includes frontend URL
- Verify backend is running: `http://localhost:8000/api/health`

**Backend won't start?**
- Verify Python 3.10+: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check database connection in `.env.local`

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for more troubleshooting.

## 📞 Support

For issues or questions:
1. Check [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
2. Review API docs: http://localhost:8000/docs
3. Check backend logs for errors
4. Check browser console for frontend errors

## 📄 License

See [LICENSE](./LICENSE) file

---

**Next Steps:**
1. Clone this repo
2. Follow [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
3. Deploy to Vercel and Railway
4. Enjoy your proctoring platform! 🎉

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