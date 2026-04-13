"""
ProctorForge AI - Backend Server
FastAPI application entry point with CORS, routing, and database initialization.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db
from routers.auth import router as auth_router
from routers.exams import router as exams_router
from routers.attempts import router as attempts_router
from routers.websocket import router as websocket_router
from routers.code_execution import router as code_router
from routers.monitoring import router as monitoring_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Create tables on startup
    await init_db()
    print("✅ Database tables created")
    yield
    print("🛑 Server shutting down")


app = FastAPI(
    title="ProctorForge AI",
    description="AI-native zero-trust remote assessment platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS Configuration
# This allows the frontend (Vercel) to make API calls to this backend (Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # Add Vercel domain here in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routers
app.include_router(auth_router)
app.include_router(exams_router)
app.include_router(attempts_router)
app.include_router(websocket_router)
app.include_router(code_router)
app.include_router(monitoring_router)


@app.get("/")
async def root():
    return {
        "name": "ProctorForge AI",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health():
    """Health check endpoint for deployment verification."""
    return {"status": "healthy", "service": "proctorforge-backend"}


if __name__ == "__main__":
    import uvicorn
    
    # Development mode detection
    is_development = os.getenv("ENVIRONMENT", "development") == "development"
    
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=is_development,
        workers=1 if is_development else 4,
        log_level="debug" if is_development else "info",
    )
    elapsed = int(time.time() - session_start_time)
    if elapsed < GRACE_PERIOD:
        cv2.putText(
            annotated_frame,
            f"Grace Period: {GRACE_PERIOD - elapsed}s",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

    # --------------------------------------------------
    # 🔢 Warning counter
    # --------------------------------------------------
    cv2.putText(
        annotated_frame,
        f"Warnings: {warning_count}/{MAX_WARNINGS}",
        (30, 260),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    if warning_count >= MAX_WARNINGS:
        log_event(log_file, "DISQUALIFIED", "Too many warnings", warning_count)
        save_screenshot(frame, session_id, "Too_many_warnings")
        break

    cv2.imshow("AI Proctoring System", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
