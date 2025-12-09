"""
Path: server/app/main.py
Purpose: FastAPI application entry point with CORS and router registration
Logic:
  - Creates FastAPI app instance
  - Adds CORS middleware for local dev (allows localhost:5173)
  - Registers combat and saves routers
  - Provides health check endpoints
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import combat, saves

app = FastAPI(
    title="Faerun Combat Server",
    description="Backend for side-scroller combat game",
    version="0.1.0"
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(combat.router, prefix="/api/combat", tags=["combat"])
app.include_router(saves.router, prefix="/api/saves", tags=["saves"])


@app.get("/")
async def root():
    return {"message": "Faerun Combat Server", "status": "online"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
