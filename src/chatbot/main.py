from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "ACA FastAPI is running",
        "environment": os.getenv("ENV", "unknown")
    }

@app.get("/health")
def health():
    return {"health": "healthy"}
