# vectorstore.py
import json
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings  # Local & free

def load_chunks(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def create_vectorstore(path: str = "data/superior-outreach_chunks.jsonl"):
    chunks = load_chunks(path)
    docs = [Document(page_content=chunk["text"], metadata={"id": chunk["id"]}) for chunk in chunks]

    # Embedding model: change if needed
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Optional: re-split for consistent chunking
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(split_docs, embedding)
    return vectorstore
