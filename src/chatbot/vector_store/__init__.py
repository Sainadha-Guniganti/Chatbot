
from langchain_azure_storage.document_loaders import AzureBlobStorageLoader
from langchain_community.document_loaders import PyPDFLoader
from azure.identity import DefaultAzureCredential
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import AzureSearch

from chatbot.config import ChatbotConfig




def load_blob_config(storage_account_url:str,container_name:str) -> AzureBlobStorageLoader:
    loader = AzureBlobStorageLoader(
        account_url=storage_account_url,
        container_name=container_name,
        credential=DefaultAzureCredential(),
        loader_factory=PyPDFLoader
    )
    return loader

def get_text_splitter(chunk_size:int, chunk_overlap:int) -> RecursiveCharacterTextSplitter:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter

def azure_vector_store(
    app_config: ChatbotConfig,
    embedding_function    
) -> AzureSearch:
    azure_search = AzureSearch(
        azure_search_endpoint = app_config.INDEX_ENDPOINT,
        embedding_function = embedding_function,
        index_name = app_config.INDEX_NAME,
        azure_search_key = app_config.KEY,
    )
    return azure_search