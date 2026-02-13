# save_vectorstore.py

import json
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings  # Only needed here

def load_chunks(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def build_and_save_vectorstore():
    chunks = load_chunks("data/superior-outreach_chunks.jsonl")
    docs = [Document(page_content=chunk["text"], metadata={"id": chunk["id"]}) for chunk in chunks]

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embedding)

    vectorstore.save_local("vectorstore")
    print("✅ Vectorstore saved to /vectorstore")

if __name__ == "__main__":
    build_and_save_vectorstore()
