from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# -------------------------
# FastAPI App
# -------------------------
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

# -------------------------
# Azure OpenAI Client
# -------------------------
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

endpoint= os.getenv("AZURE_OPENAI_ENDPOINT"),

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# -------------------------
# Request / Response Models
# -------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# -------------------------
# Chatbot Endpoint
# -------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        completion = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful enterprise AI assistant."},
                {"role": "user", "content": request.message}
            ],
            temperature=1,
            max_completion_tokens=5000
        )

        return ChatResponse(
            response=completion.choices[0].message.content
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Azure OpenAI error: {str(e)}"
        )
