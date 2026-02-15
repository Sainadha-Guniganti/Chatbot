from pydantic_settings import BaseSettings, SettingsConfigDict

class ChatbotConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_KEY: str

    MANAGED_IDENTITY_CLIENT_ID: str
    COGNITIVE_SERVICE_SCOPE: str

    # Embeddings
    OPENAI_TEXT_EMBEDDING_ENDPOINT: str
    OPENAI_TEXT_EMBEDDING_API_VERSION: str
    OPENAI_TEXT_EMBEDDING_DEPLOYMENT_NAME: str

    SEARCH_SERVICE_SCOPE: str
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int

    # Azure AI Search
    INDEX_ENDPOINT: str
    KEY: str
    INDEX_NAME: str
    VECTOR_DIMENSIONS: int

    # Storage
    CONTAINER_NAME: str
    ACCOUNT_URL: str


app_config = ChatbotConfig()
