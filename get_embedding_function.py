import os
from langchain_community.embeddings.ollama import OllamaEmbeddings

OLLAMA_SERVER_URL = os.getenv('OLLAMA_SERVER_URL', 'http://localhost:11434')
MODEL = os.getenv('MODEL', 'mistral')


def get_embedding_function():
    embeddings = OllamaEmbeddings(base_url=OLLAMA_SERVER_URL, model=MODEL)
    return embeddings
