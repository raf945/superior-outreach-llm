import os
import logging
from typing import Dict, Deque
from collections import deque, defaultdict
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from openai import AsyncOpenAI  # Use Async Client
from dotenv import load_dotenv
from cachetools import TTLCache

# Setup logging (Safe for production)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# ✅ Initialize Async Client
# Ensure OPENAI_API_KEY is in your environment variables, not code!
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# ✅ Secure Memory: Keeps max 1000 sessions, expires them after 1 hour (3600s)
# This prevents RAM exhaustion attacks.
session_cache = TTLCache(maxsize=1000, ttl=3600)
chat_memory: Dict[str, Deque] = defaultdict(lambda: deque(maxlen=5))

# Wrapper to link cachetools with your deque structure
def get_chat_history(session_id: str):
    if session_id not in session_cache:
        session_cache[session_id] = deque(maxlen=5)
    return session_cache[session_id]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.superioroutreach.ai",
        "https://superioroutreach.ai",
        "https://superior-outreach-chatbot.onrender.com",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], # Restrict methods to what you use
    allow_headers=["Authorization", "Content-Type"], # Restrict headers
)

# ✅ Standard StaticFiles is usually sufficient for .js
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="static")

# ✅ Input Validation (Prevents huge payloads)
class PromptRequest(BaseModel):
    message: str = Field(..., max_length=2000, description="Limit input to 2000 chars")
    session_id: str = Field(..., max_length=100, pattern="^[a-zA-Z0-9_-]+$")

@app.get("/superioroutreach")
async def blank():
    return FileResponse("frontend/superior-outreach.html")

# Async Endpoint
@app.post("/chat")
async def chat_with_llm(request: PromptRequest):
    try:
        session_id = request.session_id
        user_query_raw = request.message.strip()

        # Retrieve history safely
        history = get_chat_history(session_id)

        # (Placeholder for your vectorstore logic)
        # relevant_docs = await vectorstore.asimilarity_search(user_query_raw, k=3) 
        # For this example, we assume context is empty string if vectorstore is missing
        context = "" 

        logger.info(f"Session {session_id}: Processing message")

        # ✅ Use Async Call
        response = await client.chat.completions.create(
            model="gpt-4o-mini", # Corrected model name (check availability)
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful sales assistant. "
                        "Keep answers under 3 sentences. "
                        f"Context: {context}"
                    )
                },
                {"role": "user", "content": user_query_raw}
            ]
        )

        assistant_message = response.choices[0].message.content or "No response."

        # Update Memory
        history.append({"role": "user", "content": user_query_raw})
        history.append({"role": "assistant", "content": assistant_message})

        return {"response": assistant_message}

    except Exception as e:
        # ✅ Secure Error Handling
        logger.error(f"Error processing chat: {e}") # Log the real error for YOU
        # Return generic error to USER
        raise HTTPException(status_code=500, detail="Internal Service Error")