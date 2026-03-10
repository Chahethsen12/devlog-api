from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.models

from app.routes import auth, logs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevLog API",description="A developer activity logging API — track what you build, how long, and how you felt.",version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(logs.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "🚀 DevLog API is running! 🚀"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}