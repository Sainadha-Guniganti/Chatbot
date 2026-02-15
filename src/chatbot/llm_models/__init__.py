from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI

from chatbot.config import ChatbotConfig


# --->DEPLOYMENT WITH MANAGED IDENTITY(ONLY WORK WITHIN AZURE VM,AKS,ACA)<---
# credential = ManagedIdentityCredential(
#     client_id=MANAGED_IDENTITY_CLIENT_ID
# )
# def token_provider():
#     token = credential.get_token(COGNITIVE_SERVICE_SCOPE)
#     return token.token

#--->LOCAL AUTHENTICATION FOR AZURE SERVICES<---

def load_llm_model(app_config: ChatbotConfig) -> AzureChatOpenAI:
    client = AzureChatOpenAI(
        azure_deployment=app_config.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version=app_config.AZURE_OPENAI_API_VERSION,
        azure_endpoint=app_config.AZURE_OPENAI_ENDPOINT,
        api_key=app_config.AZURE_OPENAI_API_KEY,
        temperature=0,  
        streaming=True  
    )
    return client

def load_embedding_model(app_config: ChatbotConfig) -> AzureOpenAIEmbeddings:
    client = AzureOpenAIEmbeddings(
        azure_deployment = app_config.OPENAI_TEXT_EMBEDDING_DEPLOYMENT_NAME,
        openai_api_version = app_config.OPENAI_TEXT_EMBEDDING_API_VERSION,
        azure_endpoint = app_config.OPENAI_TEXT_EMBEDDING_ENDPOINT,
        azure_ad_token_provider= get_bearer_token_provider(DefaultAzureCredential(), app_config.COGNITIVE_SERVICE_SCOPE)
    )
    return client