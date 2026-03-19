import io
from pathlib import Path
import re
from urllib.parse import quote

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from services import generate_response, synthesize_speech

load_dotenv(Path(__file__).resolve().parent / ".env")

app = FastAPI(title="Echo Voice Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_history: list[dict[str, str]] = []
SUPPORTED_LANGUAGES = {"en-US", "ta-IN", "hi-IN"}
SCRIPT_PATTERNS = {
    "ta-IN": re.compile(r"[\u0B80-\u0BFF]"),
    "hi-IN": re.compile(r"[\u0900-\u097F]"),
    "en-US": re.compile(r"[A-Za-z]"),
}


class ChatRequest(BaseModel):
    text: str
    language: str = "en-US"


def _get_message(request: ChatRequest) -> str:
    message = request.text.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Text is required.")
    return message


def _get_requested_language(request: ChatRequest) -> str:
    language = request.language.strip() if request.language else "en-US"
    if language not in SUPPORTED_LANGUAGES:
        return "en-US"
    return language


def _detect_language_from_message(message: str, fallback: str = "en-US") -> str:
    counts = {
        language: len(pattern.findall(message))
        for language, pattern in SCRIPT_PATTERNS.items()
    }

    dominant_language = max(counts, key=counts.get)
    dominant_count = counts[dominant_language]

    if dominant_count == 0:
        return fallback if fallback in SUPPORTED_LANGUAGES else "en-US"

    ties = [language for language, count in counts.items() if count == dominant_count]
    if len(ties) > 1:
        if fallback in ties:
            return fallback
        if "en-US" in ties:
            return "en-US"

    return dominant_language


def _get_language(request: ChatRequest, message: str) -> str:
    requested_language = _get_requested_language(request)
    return _detect_language_from_message(message, fallback=requested_language)


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "Echo is running"}


@app.post("/chat")
def chat(request: ChatRequest) -> StreamingResponse:
    message = _get_message(request)
    language = _get_language(request, message)

    try:
        response_text = generate_response(message, conversation_history, language=language)
        audio_bytes = synthesize_speech(response_text, language=language)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    headers = {
        "X-Echo-Text": quote(response_text, safe=""),
        "Access-Control-Expose-Headers": "X-Echo-Text",
    }
    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers=headers,
    )
