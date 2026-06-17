import chromadb

from app.core.settings import settings


def get_chromadb_collection():
    chroma_client = chromadb.PersistentClient(path=settings.chroma_db_path)
    return chroma_client.get_or_create_collection(settings.chroma_collection_name)
