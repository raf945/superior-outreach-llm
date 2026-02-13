# vectorstore.py

from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

# Lightweight dummy embedder (no transformer loaded)
class DummyEmbeddings(Embeddings):
    def embed_query(self, text: str):
        return [0.0] * 384  # match dimension used when saving

    def embed_documents(self, texts):
        return [[0.0] * 384 for _ in texts]

def create_vectorstore():
    embedding = DummyEmbeddings()
    return FAISS.load_local("vectorstore", embedding, allow_dangerous_deserialization=True)
