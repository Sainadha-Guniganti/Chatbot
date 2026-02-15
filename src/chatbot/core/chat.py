from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser

from chatbot.config import ChatbotConfig
from chatbot.llm_models import load_llm_model
from chatbot.prompts import chat_prompt
from chatbot.core.retriever import get_retrieved_context
from chatbot.logs.logger import logger


def create_chat_chain(app_config: ChatbotConfig) -> Runnable:

    llm = load_llm_model(app_config)
    chat_chain = chat_prompt | llm | StrOutputParser()

    return chat_chain


def process_chat_response(
    query: str,
    chat_chain: Runnable,
    app_config: ChatbotConfig
) -> str:
    
    retrieved_context = get_retrieved_context(query, app_config)



    try:
        logger.debug(f"Invoking chain for query: {query}")
        response = chat_chain.invoke(
            input={
                "query": query,
                "retrieved_context": retrieved_context
            }
        )
        return response
    except Exception as e:
        logger.error(f"Chain invocation failed: {e}")
        return f"Error generating response: {str(e)}"
    
    