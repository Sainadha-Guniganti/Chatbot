from typing import List

from langchain_core.documents import Document

from chatbot.config import ChatbotConfig
from chatbot.llm_models import load_embedding_model
from chatbot.vector_store import azure_vector_store


def get_retrieved_context(query: str, app_config:ChatbotConfig) -> str:

    embedding_model = load_embedding_model(app_config=app_config)
    vector_store = azure_vector_store(app_config=app_config, embedding_function=embedding_model.embed_query)
    docs = vector_store.similarity_search(
        query=query,
        k=3,
        search_type="similarity"
    )
    def format_docs(docs: List[Document]) -> str:
        """Formats retrieved documents into a single string context."""
        if not docs:
            return "No relevant documents found."
            
        formatted_chunks = []
        for doc in docs:
            # Extract metadata safely
            source = doc.metadata.get("doc_name", "Unknown Source")
            page = doc.metadata.get("page_no", "?")
            
            # Clean content (remove excessive newlines)
            content = doc.page_content.replace("\n", " ").strip()
            
            # Format: [Source: file.pdf, Page: 1] Content...
            formatted_chunks.append(f"[Source: {source}, Page: {page}]\n{content}")
            
        return "\n\n".join(formatted_chunks)
    return format_docs(docs)

