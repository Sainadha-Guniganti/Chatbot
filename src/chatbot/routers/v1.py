
from fastapi.routing import APIRouter
from fastapi import HTTPException

from chatbot.models.api import ChatRequest,ChatResponse
from chatbot.config import app_config
from chatbot.logs.logger import logger
from chatbot.vector_store.load_index import process_load_docs_to_index
from chatbot.core.chat import create_chat_chain, process_chat_response


router = APIRouter(prefix="/api/v1",tags=["v1-api"])

@router.get("/health")
def health():
    return {"health": "healthy"}


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    log = logger.bind(user_query = request.message)

    log.info("recieved chat request from user")
    try:
        chat_chain = create_chat_chain(app_config=app_config)
        response = process_chat_response(
            query=request.message,
            app_config=app_config,
            chat_chain=chat_chain
        )

        return {"answer": response}

    except Exception as e:
        log.exception("Failed to generate response")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/load_index")
def load_index() :
    result = process_load_docs_to_index(app_config=app_config)
