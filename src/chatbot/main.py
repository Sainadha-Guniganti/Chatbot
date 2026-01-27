from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import AzureOpenAI
from azure.identity import ManagedIdentityCredential

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
AZURE_OPENAI_ENDPOINT= os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
MANAGED_IDENTITY_CLIENT_ID = os.getenv("MANAGED_IDENTITY_CLIENT_ID")


credential = ManagedIdentityCredential(
    client_id=MANAGED_IDENTITY_CLIENT_ID
)



client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_ad_token_provider=credential.get_token
)


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
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful enterprise AI assistant."},
                {"role": "user", "content": request.message}
            ],
            temperature=1,
            max_tokens=5000
        )

        return ChatResponse(
            response=completion.choices[0].message.content
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Azure OpenAI error: {str(e)}"
        )
