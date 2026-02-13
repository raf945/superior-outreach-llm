from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

response = client.responses.create(
    model="o4-mini-2025-04-16",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)