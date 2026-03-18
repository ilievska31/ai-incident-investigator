from langchain_community.vectorstores import Chroma
from .embeddings import get_embeddings

def get_vectorstore():
    return Chroma(
        collection_name="memory",
        embedding_function=get_embeddings(),
        persist_directory="./incident_db"
    )