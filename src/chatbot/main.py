import os 

from fastapi import FastAPI
import uvicorn

from chatbot.routers.v1 import router

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "ACA FastAPI is running",
        "environment": os.getenv("ENV", "unknown")
    }

app.include_router(router)


# -------------------------
# Chatbot Endpoint
# -------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host= "0.0.0.0", port= 8000, reload= True)