from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.config.settings import settings
from backend.config.database import init_db

from backend.routes import generator, analytics, evaluation

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 {settings.APP_NAME} starting...")
    init_db()
    yield
    print(f"🛑 {settings.APP_NAME} shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered app blueprint generator",
    version="1.0.0",
    lifespan=lifespan
)

# CORS — single block, no duplicates
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(generator.router)
app.include_router(analytics.router)
app.include_router(evaluation.router)

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "app": settings.APP_NAME
    }