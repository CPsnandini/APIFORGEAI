from google import genai
from google.genai import types
from config import Config

_client = None

MODEL_NAME = "gemini-2.5-flash"


def get_client():
    global _client
    if _client is None:
        if not Config.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set in .env")
        _client = genai.Client(
            api_key=Config.GEMINI_API_KEY,
            http_options=types.HttpOptions(
                timeout=20000,  # 20 seconds per attempt, in milliseconds
                retry_options=types.HttpRetryOptions(
                    attempts=2,       # original call + 1 retry, not the default 5
                    initial_delay=1.0,
                    max_delay=5.0,
                ),
            ),
        )
    return _client


def ask_gemini(prompt):
    client = get_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text