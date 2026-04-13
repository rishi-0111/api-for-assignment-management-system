# ProctorForge AI - Full Stack Proctoring Platform

> A comprehensive AI-native zero-trust remote assessment platform with advanced proctoring capabilities

## 📁 Project Structure

This is a **monorepo** containing the frontend and backend applications:

```
.
├── frontend/              # Next.js frontend application (Vercel)
│   ├── src/
│   ├── package.json
│   ├── vercel.json
│   ├── .env.example
│   └── .env.local         # Local dev config (git-ignored)
│
├── backend/               # FastAPI backend application (Railway)
│   ├── routers/
│   ├── models/
│   ├── services/
│   ├── main.py
│   ├── requirements.txt
│   ├── railway.json
│   ├── .env.example
│   └── .env.local         # Local dev config (git-ignored)
│
└── DEPLOYMENT_GUIDE.md    # Complete deployment instructions
```

## 🚀 Quick Start (Local Development)

### Backend Setup

```bash
cd backend
python -m venv venv
# Activate: venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
cp .env.example .env.local
python main.py  # Runs on http://localhost:8000
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev  # Runs on http://localhost:3000
```

## 🌐 Production Deployment

### Deploy Backend to Railway

1. Push code to GitHub
2. Go to https://railway.app
3. Create new project → Import from GitHub
4. Select repository, set root directory to `backend/`
5. Add environment variables from `backend/.env.example`
6. Railway auto-deploys on git push

### Deploy Frontend to Vercel

1. Go to https://vercel.com/new
2. Import GitHub repository
3. Set root directory to `frontend/`
4. Add environment variables pointing to Railway backend
5. Deploy!

## 📚 Features

- ✅ **AI-Powered Proctoring**: Real-time monitoring with AI Twin interventions
- ✅ **Code Execution**: Sandboxed code execution environment
- ✅ **Live Exams**: WebSocket-based live exam sessions
- ✅ **Real-Time Analytics**: Instant insights and performance metrics
- ✅ **Multi-Format Exams**: MCQ, coding challenges, and more
- ✅ **Zero-Trust Security**: Advanced security features
- ✅ **Database Logging**: Comprehensive audit trails

## 🔧 Environment Variables

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Backend (`backend/.env.local` for dev, `backend/.env` for production)
```env
DATABASE_URL=sqlite+aiosqlite:///./proctorforge.db?check_same_thread=false
JWT_SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

See `backend/.env.example` for all environment variables.

## 📖 Documentation

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Complete setup and deployment guide
- **Backend API Docs**: http://localhost:8000/docs (when running locally)
- **Backend Redoc**: http://localhost:8000/redoc

## 🛠 Tech Stack

### Frontend
- **Next.js 16+** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Socket.io** - Real-time communication
- **Zustand** - State management

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM
- **PostgreSQL/Supabase** - Database
- **Redis** - Caching & WebSockets
- **Docker** - Containerization

## 🔐 Security

- JWT-based authentication
- CORS configuration for production
- HMAC event signing
- Zero-trust architecture
- Sandboxed code execution

## 📝 License

See [LICENSE](./LICENSE) file

## 👥 Contributors

ProctorForge AI Team

---

For detailed setup and deployment instructions, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
