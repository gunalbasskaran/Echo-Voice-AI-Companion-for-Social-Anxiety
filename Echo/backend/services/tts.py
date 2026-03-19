import base64
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MURF_API_KEY = os.getenv("MURF_API_KEY")
MURF_ENDPOINT = "https://api.murf.ai/v1/speech/generate"
DEFAULT_VOICE_ID = "en-US-cooper"
VOICE_BY_LANGUAGE = {
    "en-US": "en-US-cooper",
    "ta-IN": "ta-IN-mayil",
    "hi-IN": "hi-IN-shaan",
}


def _extract_audio_bytes(response: requests.Response) -> bytes:
    if response.headers.get("Content-Type", "").startswith("audio/"):
        return response.content

    data = response.json()
    audio_base64 = data.get("audioContent") or data.get("audio")
    if audio_base64:
        return base64.b64decode(audio_base64)

    audio_url = data.get("audioFile") or data.get("audioUrl") or data.get("url")
    if audio_url:
        audio_response = requests.get(audio_url, timeout=90)
        audio_response.raise_for_status()
        return audio_response.content

    raise ValueError("Murf API response did not include audio data.")


def _request_synthesis(text: str, voice_id: str, headers: dict[str, str]) -> bytes:
    payload = {"text": text, "voiceId": voice_id, "format": "mp3"}
    response = requests.post(MURF_ENDPOINT, headers=headers, json=payload, timeout=90)
    response.raise_for_status()
    return _extract_audio_bytes(response)


def synthesize_speech(text: str, language: str = "en-US") -> bytes:
    if not MURF_API_KEY:
        raise ValueError("MURF_API_KEY is missing from environment variables.")

    headers = {"api-key": MURF_API_KEY, "Content-Type": "application/json"}
    voice_id = VOICE_BY_LANGUAGE.get(language, DEFAULT_VOICE_ID)

    try:
        return _request_synthesis(text, voice_id, headers)
    except Exception:
        if voice_id == DEFAULT_VOICE_ID:
            raise
        return _request_synthesis(text, DEFAULT_VOICE_ID, headers)


if __name__ == "__main__":
    output_path = Path(__file__).resolve().parents[1] / "echo_test.mp3"
    output_path.write_bytes(synthesize_speech("Hello, I am Echo"))
    print(f"Saved {output_path.name}")
