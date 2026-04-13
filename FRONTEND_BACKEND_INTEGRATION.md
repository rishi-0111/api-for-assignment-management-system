# ProctorForge AI - Frontend & Backend Integration Guide

## 📡 How Frontend Connects to Backend

This guide explains the complete data flow and how every feature works in your separated architecture.

---

## 🏗️ Project Architecture

### Directory Structure
```
project/
├── frontend/                    # Deployed to Vercel
│   ├── src/
│   │   ├── app/                # Next.js pages
│   │   ├── components/         # React components
│   │   ├── hooks/              # Custom React hooks
│   │   ├── lib/                # Utilities (including api.ts)
│   │   └── stores/             # Zustand state management
│   ├── .env.local              # Local development (git-ignored)
│   ├── vercel.json             # Vercel deployment config
│   └── package.json
│
├── backend/                     # Deployed to Railway
│   ├── routers/                # API endpoints
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── exams.py            # Exam management
│   │   ├── attempts.py         # Exam attempts
│   │   ├── code_execution.py   # Code running
│   │   ├── monitoring.py       # Proctoring monitoring
│   │   └── websocket.py        # Real-time WebSocket  
│   ├── models/                 # Database models
│   ├── services/               # Business logic
│   ├── middleware/             # Auth middleware
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Configuration
│   ├── database.py             # Database setup
│   ├── .env                    # Production env (git-ignored)
│   └── requirements.txt        # Python dependencies
│
└── Documentation/
    ├── PRODUCTION_DEPLOYMENT.md    # Deployment guide
    ├── FRONTEND_BACKEND_INTEGRATION.md (this file)
    └── README.md
```

---

## 🔌 API Communication Pattern

### How Frontend Makes API Calls

**File**: `frontend/src/lib/api.ts`

```typescript
import axios from 'axios';

// 1. Get API URL from environment variable
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

// 2. Create Axios instance
const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// 3. Attach JWT token to all requests
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('proctorforge_token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 4. Handle 401 (unauthorized) errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== 'undefined') {
      // Token expired, redirect to login
      localStorage.removeItem('proctorforge_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

## 📊 Data Flows - Real Examples

### Flow 1: User Registration & Login

```
VERCEL FRONTEND                          RAILWAY BACKEND                    DATABASE (PostgreSQL)
┌──────────────────┐                    ┌──────────────────┐                ┌──────────────┐
│                  │                    │                  │                │              │
│ 1. User page     │                    │                  │                │              │
│    submitted:    │                    │                  │                │ Users table  │
│    - name        │                    │                  │                │   id         │
│    - email       │                    │                  │                │   name       │
│    - password    │                    │                  │                │   email      │
└────────┬─────────┘                    └──────────────────┘                └──────────────┘
         │                                                                            
         │ 2. Frontend sends POST request                                            
         │ POST /api/auth/register                                                  
         │ Body: { name, email, password }                                          
         ├─────────────────────────────────────────────────────────────────────────>
         │                                                                            
         │                              3. Backend receives request                  
         │                              4. Backend hashes password                   
         │                              5. Backend creates new User                  
         │                                                    
         │                              6. Backend inserts into Users table         
         │                              └──────────────────────────────────────────>
         │                                                                            
         │                              7. Database confirms insert                 
         │                              <───────────────────────────────────────────
         │                                                                            
         │                              8. Backend generates JWT token             
         │                              9. Backend returns { token, user }         
         │
         │ 10. Frontend receives response                                           
         │ { access_token: "jwt...", user: {...} }                                 
         │
         │ 11. Frontend stores token:                                              
         │     localStorage.proctorforge_token = "jwt..."                          
         │
         │ 12. Frontend redirects to dashboard ✓                                   
```

### Flow 2: View Exams (Protected Endpoint)

```
VERCEL FRONTEND                          RAILWAY BACKEND                    DATABASE (PostgreSQL)
┌──────────────────┐                    ┌──────────────────┐                ┌──────────────┐
│                  │                    │                  │                │              │
│ 1. Dashboard     │                    │                  │                │ Exams table  │
│    mounted       │                    │                  │                │   id         │
│                  │                    │                  │                │   name       │
└────────┬─────────┘                    └──────────────────┘                │   created_by │
         │                                                                  └──────────────┘
         │ 2. Frontend sends GET with Authorization header                            
         │ GET /api/exams                                                            
         │ Headers: {                                                                
         │   "Authorization": "Bearer eyJhbGc..."                                    
         │ }                                                                          
         ├─────────────────────────────────────────────────────────────────────────>
         │                                                                            
         │                              3. Backend receives request                 
         │                              4. Backend checks Authorization header      
         │                              5. Backend decodes JWT token                
         │                              6. Backend verifies token signature         
         │                              7. If invalid → return 401 Unauthorized     
         │                              8. If valid → extract user_id from token   
         │                                                    
         │                              9. Backend queries exams for user          
         │                              SELECT * FROM exams WHERE teacher_id = ...
         │                              └──────────────────────────────────────────>
         │                                                                            
         │                              10. Database returns exam rows             
         │                              <───────────────────────────────────────────
         │                                                                            
         │                              11. Backend formats response JSON           
         │                              12. Returns: [ {id, name, ...}, ... ]      
         │
         │ 13. Frontend receives exams list                                        
         │ Status: 200 OK                                                           
         │ Body: [ { id: 1, name: "Physics Exam", ... }, ... ]                     
         │
         │ 14. Frontend stores in Zustand state                                    
         │ examStore.setExams(data)                                                
         │
         │ 15. Frontend renders UI with exams ✓                                   
```

### Flow 3: Create Exam (State Management)

```
VERCEL FRONTEND
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ 1. User fills exam form:                                        │
│    - Exam name: "Mathematics Final"                             │
│    - Duration: 60 minutes                                      │
│    - Max students: 50                                           │
│                                                                 │
│ 2. User clicks "Create Exam"                                    │
│                                                                 │
│ 3. Frontend validates form:                                     │
│    if (!name) show error                                        │
│    if (duration < 0) show error                                 │
│                                                                 │
│ 4. Frontend makes API call:                                     │
│    POST /api/exams                                              │
│    Headers: { Authorization: "Bearer token" }                   │
│    Body: { name, duration, max_students }                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         │
         ├──────────────────────────────────────────────────────────────────────────>
         │
RAILWAY BACKEND
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ 5. Backend receives POST request                                │
│                                                                 │
│ 6. Backend validates:                                           │
│    - Check authorization token                                  │
│    - Validate exam data                                         │
│    - Check user exists                                          │
│                                                                 │
│ 7. Backend creates Exam object:                                │
│    exam = Exam(                                                │
│      name="Mathematics Final",                                  │
│      duration=60,                                              │
│      teacher_id=user.id,                                      │
│      max_students=50                                            │
│    )                                                            │
│                                                                 │
│ 8. Backend saves to database:                                  │
│    db.add(exam)                                                │
│    db.commit()   → INSERT INTO exams (name, duration, ...) ... │
│                                                                 │
│ 9. Backend returns response:                                   │
│    { id: 42, name: "Mathematics Final", ... }                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         │
         │<─────────────────────────────────────────────────────────────────────────
         │
VERCEL FRONTEND
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ 10. Frontend receives response:                                 │
│     Status: 201 Created                                         │
│     Body: { id: 42, name: "Mathematics Final", ... }           │
│                                                                 │
│ 11. Frontend updates Zustand store:                             │
│     examStore.addExam(newExam)                                  │
│                                                                 │
│ 12. Frontend shows success notification:                        │
│     "Exam created successfully!"                                │
│                                                                 │
│ 13. Frontend redirects to exam details page ✓                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 WebSocket Real-Time Communication

### Live Exam Monitoring (WebSocket)

```
VERCEL FRONTEND                          RAILWAY BACKEND
┌──────────────────┐                    ┌──────────────────┐
│ Teacher Dashboard│                    │ WebSocket Router │
│                  │                    │                  │
│ Monitoring:      │                    │ Maintains:       │
│ - Live students  │                    │ - Connections    │
│ - Scores         │                    │ - Sessions       │
│ - Status         │                    │ - Events         │
└────────┬─────────┘                    └────────┬─────────┘
         │                                        │
         │ 1. Establish WebSocket Connection     │
         │ ws://backend/ws/exam/123/teacher     │
         ├─────────────────────────────────────>│
         │                                        │
         │ 2. Backend validates connection       │
         │ - Check JWT token                     │
         │ - Register teacher in session         │
         │                                        │
         │ 3. Confirmation message ◄─────────────┤
         │                                        │
         │────────────────────────────────────────│
         │                                        │
         │ 4. Student submits answer             │
         │                                        │
         │                                        │ 5. Backend receives answer event
         │                                        │    - Validates answer
         │                                        │    │ 6. Save to database
         │                                        │    └─────────────────────>
         │                                        │
         │ 7. Backend broadcasts to teacher:  ◄──┤
         │ {                                      │
         │   "type": "student_answered",          │
         │   "student_id": 456,                   │
         │   "question_id": 789,                  │
         │   "timestamp": "2024-04-13T..."        │
         │ }                                      │
         │                                        │
         │ 8. Frontend updates UI                │
         │    - Shows live scores                │
         │    - Updates student status           │
         │    - Shows real-time progress ✓       │
```

---

## 🗄️ Database Operations - All Through APIs

### User Lifecycle

```
1. REGISTRATION
   Frontend → POST /api/auth/register → Backend → INSERT INTO users
   
2. LOGIN
   Frontend → POST /api/auth/login → Backend → SELECT FROM users WHERE email
   
3. GET PROFILE
   Frontend → GET /api/auth/me → Backend → SELECT FROM users WHERE id = current_user
   
4. UPDATE PROFILE
   Frontend → PATCH /api/auth/users/{id} → Backend → UPDATE users SET ...
   
5. DELETE USER
   Frontend → DELETE /api/auth/users/{id} → Backend → DELETE FROM users WHERE id
```

### Exam Lifecycle

```
1. CREATE EXAM
   Frontend → POST /api/exams → Backend → INSERT INTO exams
   
2. LIST EXAMS
   Frontend → GET /api/exams → Backend → SELECT * FROM exams WHERE teacher_id
   
3. GET EXAM DETAILS
   Frontend → GET /api/exams/{id} → Backend → SELECT FROM exams WHERE id
   
4. UPDATE EXAM
   Frontend → PATCH /api/exams/{id} → Backend → UPDATE exams SET ...
   
5. DELETE EXAM
   Frontend → DELETE /api/exams/{id} → Backend → DELETE FROM exams WHERE id
```

### Exam Attempt Lifecycle

```
1. START ATTEMPT
   Frontend → POST /api/attempts → Backend → INSERT INTO attempts
   
2. SUBMIT ANSWER
   Frontend → POST /api/attempts/{id}/answers → Backend → INSERT INTO answers
   
3. GET ATTEMPT STATUS
   Frontend → GET /api/attempts/{id} → Backend → SELECT FROM attempts
   
4. SUBMIT EXAM
   Frontend → POST /api/attempts/{id}/submit → Backend → UPDATE attempts SET complete
   
5. VIEW RESULTS
   Frontend → GET /api/attempts/{id}/results → Backend → SELECT answers, grade
```

---

## 🔐 Authentication Implementation

### JWT Token Flow

```
┌─ Local Development ─┐          ┌─ Production (Vercel + Railway) ─┐
│                    │           │                                  │
│ User logs in:      │           │ User logs in on app.vercel.app:  │
│ localhost:3000     │           │                                  │
│                    │           │ Frontend sends          ←────────┼─→ Railway Backend
│ Frontend POST      │           │ POST /api/auth/login            │
│ localhost:8000     │           │ Header: Authorization           │
│                    │           │                                  │
│ Backend generates  │           │ Backend verifies & returns:      │
│ JWT Token:         │           │ { token: "eyJ..." }            │
│ eyJ...             │           │                                  │
│                    │           │ Frontend stores in localStorage  │
│                    │           │                                  │
│ Subsequent requests │          │ All requests include:            │
│ include:           │           │ Authorization: Bearer eyJ...    │
│ Authorization:     │           │                                  │
│ Bearer eyJ...      │           │ Backend verifies token validity │
│                    │           │ If valid → process request      │
│                    │           │ If invalid → 401 Unauthorized   │
└────────────────────┘           └──────────────────────────────────┘
```

### Token Storage & Security

```javascript
// Frontend stores token in localStorage
localStorage.setItem('proctorforge_token', token)

// Frontend sends with every request via Axios interceptor
api.interceptors.request.use(config => {
  const token = localStorage.getItem('proctorforge_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Backend validates JWT signature
verify_token(token) → extract user_id → proceed

// On logout or 401
localStorage.removeItem('proctorforge_token')
redirect to /login
```

---

## 📡 API Endpoints Reference

### Authentication Endpoints

```
POST   /api/auth/register
       Body: { name, email, password, role, ...extras }
       Returns: { access_token, user }

POST   /api/auth/login
       Body: { email, password }
       Returns: { access_token, user }

GET    /api/auth/me
       Headers: { Authorization: Bearer ... }
       Returns: { id, name, email, role, ...}

GET    /api/auth/users
       Headers: { Authorization: Bearer ... }
       Returns: [{ id, name, email, role, ... }]

PATCH  /api/auth/users/{user_id}/status
       Headers: { Authorization: Bearer ... }
       Body: { status_val }
       Returns: { id, status }

DELETE /api/auth/users/{user_id}
       Headers: { Authorization: Bearer ... }
       Returns: {success: true}
```

### Exam Endpoints

```
GET    /api/exams
       Returns list of exams

POST   /api/exams
       Body: { name, description, duration, max_students, ... }
       Returns: created exam

GET    /api/exams/{exam_id}
       Returns exam details

PATCH  /api/exams/{exam_id}
       Body: updated fields
       Returns: updated exam

DELETE /api/exams/{exam_id}
       Returns: {success: true}

POST   /api/exams/{exam_id}/questions
       Body: question data
       Returns: created question
```

### Attempt Endpoints

```
POST   /api/attempts
       Body: { exam_id, student_id }
       Returns: { attempt_id, exam, ... }

GET    /api/attempts/{attempt_id}
       Returns: attempt details

POST   /api/attempts/{attempt_id}/answers
       Body: { question_id, answer }
       Returns: {success: true}

POST   /api/attempts/{attempt_id}/submit
       Returns: { score, result }

GET    /api/attempts/{attempt_id}/results
       Returns: { score, answers, feedback }
```

---

## 🐛 Debugging & Testing

### Check Network Requests

```javascript
// In browser console
// See what URL is being used
console.log(process.env.NEXT_PUBLIC_API_URL)
// Expected: https://your-backend.railway.app

// Make a test request
fetch('https://your-backend/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
// Expected: {status: "healthy", service: "proctorforge-backend"}
```

### Check Token Storage

```javascript
// In browser console
const token = localStorage.getItem('proctorforge_token')
console.log(token)
// If null → not logged in
// If exists → logged in

// Decode JWT to see contents
// Use https://jwt.io
```

### Check API Logs

**Railway Backend Logs:**
```bash
# View real-time logs
# In Railway Dashboard → Services → Backend → Logs

# Look for:
# ✅ POST /api/auth/login 200
# ✅ GET /api/exams 200
# ❌ GET /api/exams 401 (unauthorized)
# ❌ POST /api/exams 403 (forbidden)
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| CORS error | Backend doesn't allow origin | Update CORS_ORIGINS in Railway |
| 401 Unauthorized | Invalid/expired token | Login again |
| 403 Forbidden | Don't have permission | Check user role |
| 404 Not Found | Endpoint doesn't exist | Check URL spelling |
| 500 Internal Error | Backend crashed | Check Railway logs |
| Network Error | Can't reach backend | Check if Railway is running |

---

## 🎯 Testing Complete Integration

### Test Login Flow

```
1. Go to your Vercel app → Login page
2. Open DevTools (F12) → Network tab
3. Enter email & password
4. Submit
5. See POST /api/auth/login
6. Check response → should include token
7. Confirm redirect to dashboard
8. Check localStorage → proctorforge_token should exist
✓ Integration working!
```

### Test Data Loading

```
1. Go to Dashboard
2. Open DevTools (F12) → Network tab
3. See GET /api/exams
4. Check response → should show exams
5. Verify data displays on page
✓ Integration working!
```

### Test Create Feature

```
1. Click "Create Exam"
2. Fill form & submit
3. Open DevTools (F12) → Network tab
4. See POST /api/exams
5. Check response status: 201
6. Verify exam appears in list
7. Refresh page → data persists
✓ Integration working!
```

---

## 📚 Related Files

- **Frontend API Client**: `frontend/src/lib/api.ts`
- **Authentication Store**: `frontend/src/stores/authStore.ts`
- **Backend Main App**: `backend/main.py`
- **Backend Config**: `backend/config.py`
- **Backend Auth Router**: `backend/routers/auth.py`
- **Backend Exams Router**: `backend/routers/exams.py`
- **Deployment Guide**: `PRODUCTION_DEPLOYMENT.md`
- **Environment Variables**: See `.env.example` files

---

## ✅ Verification Checklist

- [ ] Frontend makes API calls (not direct database)
- [ ] All requests use HTTPS in production
- [ ] JWT tokens are used for authentication
- [ ] CORS allows Vercel domain on Railway
- [ ] All data flows through API routes
- [ ] No hardcoded URLs in frontend
- [ ] No database credentials exposed in frontend
- [ ] Error handling works (401 redirects to login)
- [ ] WebSocket connections work
- [ ] Real-time updates display correctly
- [ ] Features work end-to-end

**If all checked ✓ → Your integration is production-ready!**
