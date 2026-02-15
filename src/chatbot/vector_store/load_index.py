from typing import Dict,Any

from langchain_community.vectorstores import AzureSearch
from langchain_core.documents import Document
import uuid

from chatbot.vector_store import load_blob_config,get_text_splitter,azure_vector_store
from chatbot.config import ChatbotConfig
from chatbot.llm_models import load_embedding_model
from chatbot.logs.logger import logger


def add_metadata_to_chunks(split_docs:list[Document]):
    final_chunks = []
    for i, doc in enumerate(split_docs):
        source_file = doc.metadata.get("source", "unknown")
        page_num = doc.metadata.get("page", 0)
        
        chunk_id = str(uuid.uuid1())
        
        cleaned_content = doc.page_content.replace("\x00", "").strip()
        
        chunk_payload = {
            "id": chunk_id,
            "content": cleaned_content,
            "doc_name": source_file.split("/")[-1],
            "page_no": page_num,
            "chunk_index": i,
            "metadata_json": doc.metadata
        }
    
        final_chunks.append(chunk_payload)
    return final_chunks

def load_docs_to_index(final_chunks : Dict,vector_store : AzureSearch) -> Any:
    docs_to_upload = [
    Document(
        page_content=chunk["content"], 
        metadata=chunk["metadata_json"]
    ) 
    for chunk in final_chunks
    ]
    try:

        vector_store.add_documents(documents = docs_to_upload)
        logger.success("loaded documents to index successfully")
        return True
    except Exception as e:
        logger.error(f"unable to load index - error : {e}")
        return False
    


def process_load_docs_to_index(app_config: ChatbotConfig):
    loader = load_blob_config(app_config.ACCOUNT_URL, app_config.CONTAINER_NAME)

    documents = loader.load()

    splitter = get_text_splitter(app_config.CHUNK_SIZE,app_config.CHUNK_OVERLAP)

    split_docs = splitter.split_documents(documents)
    final_chunks = add_metadata_to_chunks(split_docs)

    embedding_model = load_embedding_model(app_config)
    vector_store = azure_vector_store(
        app_config,
        embedding_model.embed_query,
    )
    print(vector_store)
    result1 = load_docs_to_index(final_chunks,vector_store)
    if result1:
        print("✅ Upload complete!")
    else:
        print("❌ Upload failed.")






