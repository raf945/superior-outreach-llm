from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from mimetypes import guess_type
from collections import defaultdict
from pydantic import BaseModel
from collections import defaultdict, deque
import requests
import anyio
import os

from vectorstore import create_vectorstore

vectorstore = create_vectorstore()

# ✅ App instance
app = FastAPI()

# ✅ In-memory chat history
chat_memory = defaultdict(lambda: deque(maxlen=5))

# ✅ CORS for Wix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.superioroutreach.ai"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Custom static server to fix JS MIME type
class CustomStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        full_path, stat_result = await anyio.to_thread.run_sync(self.lookup_path, path)
        if full_path is None:
            return self.not_found_response(path)

        content_type, _ = guess_type(full_path)
        if path.endswith(".js"):
            content_type = "application/javascript"

        return FileResponse(full_path, stat_result=stat_result, media_type=content_type)

# ✅ Serve /frontend with correct MIME
app.mount("/frontend", CustomStaticFiles(directory="frontend", html=True), name="static")

# ✅ Together API setup
TOGETHER_API_KEY = "b3265da6fdcd075f8c7ace9f205cd555bd9c3e506986b5feed407fcf6e2f2822"
TOGETHER_ENDPOINT = "https://api.together.xyz/v1/chat/completions"

# ✅ Request schema
class PromptRequest(BaseModel):
    message: str
    session_id: str

# Fresh deploy

@app.post("/chat")
def chat_with_llm(request: PromptRequest):

    session_id = request.session_id
    user_query = request.message

    # Step 1: Perform similarity search
    relevant_docs = vectorstore.similarity_search(user_query, k=3)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Step 2: Format prompt with context
    system_prompt = (
        "You are a concise and helpful assistant. "
        "Only answer the user's question. Do not provide extra context, marketing details, or unrelated information. "
        "If the answer is in the context below, respond directly and briefly (1–2 sentences max)."
        "In your responses act as if you are talking to a 16 year old mature adult with a high school education in english"
        "Also be a bit friendly"
        "You can include only 1-2 relevant emojis charactors IN TOTAL to make your answer friendlier and more expressive."
        "Do not include more that 2 emoji characters or grandma will die"
        "Do not include any LINKS or anything that starts with a '[' and ends with a ']' or grandma will die"
        "\n\nContext:\n"
        f"Context:\n{context}\n\nUser question: {user_query}"
    )

    chat_memory[session_id].append({"role": "user", "content": system_prompt})
    history = chat_memory[session_id][-5:]

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": history,
        "temperature": 0.7,
        "max_tokens": 512
    }

    response = requests.post(TOGETHER_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        assistant_message = data["choices"][0]["message"]["content"]
        chat_memory[session_id].append({"role": "assistant", "content": assistant_message})
        return {"response": assistant_message}
    else:
        return {"error": response.text}


@app.get("/")
def read_root():
    return {"message": "SaaS Chatbot Prep Server Running"}



