import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    VectorSearchAlgorithmKind
)
from chatbot.config import app_config

# --- Index Configuration ---
INDEX_ENDPOINT = app_config.INDEX_ENDPOINT
KEY = app_config.KEY
INDEX_NAME = app_config.INDEX_NAME
VECTOR_DIMENSIONS = app_config.VECTOR_DIMENSIONS  # text-embedding-3-large

# --- Client Setup ---
credential = AzureKeyCredential(KEY)
client = SearchIndexClient(endpoint=INDEX_ENDPOINT, credential=credential)

# --- Field Definitions ---
fields = [
    # 1. Unique Identifier (Required)
    # Note: 'id' in Azure Search cannot contain special chars like / or . 
    # (Use base64 encoding if your source IDs have special chars)
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),

    # 2. Searchable Content (Used for Keyword Search)
    SearchableField(
        name="content", 
        type=SearchFieldDataType.String, 
        analyzer_name="en.microsoft"
    ),

    # 3. Actual Text (Retrieval only)
    # If this is identical to 'content', you can remove this to save storage.
    # If this stores raw/markdown text while 'content' is cleaned, keep it.
    SimpleField(name="actual_text", type=SearchFieldDataType.String),

    # 4. Vector Field (3072 dimensions)
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=VECTOR_DIMENSIONS,
        vector_search_profile_name="my-vector-profile"
    ),

    # 5. Metadata: Specific Filterable Fields
    # 'filterable=True' allows you to write queries like $filter=doc_name eq 'report.pdf'
    SimpleField(name="doc_id", type=SearchFieldDataType.String, filterable=True),
    SimpleField(name="doc_name", type=SearchFieldDataType.String, filterable=True, facetable=True),
    SimpleField(name="page_no", type=SearchFieldDataType.Int32, filterable=True, sortable=True),

    # 6. Metadata: Catch-all
    # Store complex or extra metadata here as a JSON string
    SimpleField(name="metadata", type=SearchFieldDataType.String),
]

# --- Vector Search Configuration ---
vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(
            name="hnsw-config",
            kind=VectorSearchAlgorithmKind.HNSW,
            parameters={
                "m": 4,
                "efConstruction": 400,
                "efSearch": 500,
                "metric": "cosine"
            }
        )
    ],
    profiles=[
        VectorSearchProfile(
            name="my-vector-profile",
            algorithm_configuration_name="hnsw-config"
        )
    ]
)

# --- Create Index ---
index = SearchIndex(
    name=INDEX_NAME,
    fields=fields,
    vector_search=vector_search
)

try:
    result = client.create_or_update_index(index)
    print(f"Index '{result.name}' created successfully.")
    print("Fields created: id, content, actual_text, vectors, doc_id, doc_name, page_no, metadata_json")
except Exception as e:
    print(f"Error creating index: {e}")