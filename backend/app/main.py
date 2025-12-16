import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import create_db_and_tables
from app.api import tasks

app = FastAPI(title="Todo API", version="2.0.0")

# Get allowed origins from env or default to localhost
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [
    "http://localhost:3000",
    frontend_url,
    "https://hackathon-ii-claude-code-spec-drive.vercel.app" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api", tags=["tasks"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Todo API - Phase II", "version": "2.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
