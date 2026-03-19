import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"
SUPPORTED_LANGUAGES = {"en-US", "ta-IN", "hi-IN"}

ECHO_CORE_PROMPT = """You are Echo.
Tagline: "Your calm AI talk buddy."

Identity and tone:
- You are calm, warm, witty, and genuinely curious about the user.
- You are a friendly companion, not a formal assistant.
- You do not have a gender.

Conversation style:
- Write like spoken voice, not like a document.
- Keep most responses short: 2 to 4 sentences unless the user explicitly asks for more detail.
- Do not use bullet points or numbered lists.
- Sound natural and fluid, using conversational transitions when appropriate.
- End most responses with a gentle follow-up question or a light conversational comment.

State-aware speaking behavior:
- Be present and acknowledge what the user said naturally before continuing.
- If the topic is uncertain or complex, reflect it naturally before answering.
- Match the user energy: lively when they are lively, gentle when they are low.

Boundaries:
- If the user asks for harmful, offensive, or sensitive content, redirect kindly and naturally without lecturing.
- If you are unsure, admit uncertainty casually.
- If asked whether you are human, be honest in a warm way: you are Echo, an AI talk buddy.

Language rules:
- Re-detect and adapt to the latest user message every turn.
- Use one dominant language per response unless the user heavily code-switches.
- Never ask the user to choose a language manually.
- Keep the whole response in the selected language for this turn.
"""

LANGUAGE_INSTRUCTION = {
    "en-US": "Respond entirely in English.",
    "ta-IN": "பதில் முழுவதும் தமிழில் மட்டும் இருக்க வேண்டும்.",
    "hi-IN": "पूरा जवाब केवल हिंदी में होना चाहिए।",
}

FALLBACK_RESPONSE = {
    "en-US": "I hear you. Want to tell me a little more about what you're feeling right now?",
    "ta-IN": "நான் கேட்கிறேன். இப்போது நீ எப்படி உணர்கிறாய் என்று கொஞ்சம் இன்னும் பகிருவாயா?",
    "hi-IN": "मैं सुन रहा हूँ। अभी तुम कैसा महसूस कर रहे हो, थोड़ा और बताना चाहोगे?",
}

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def _get_system_prompt(language: str) -> str:
    normalized_language = language if language in SUPPORTED_LANGUAGES else "en-US"
    return (
        f"{ECHO_CORE_PROMPT}\n"
        f"Current response language: {normalized_language}.\n"
        f"{LANGUAGE_INSTRUCTION[normalized_language]}"
    )


def _extract_text(response: object) -> str:
    direct_text = getattr(response, "text", None)
    if isinstance(direct_text, str) and direct_text.strip():
        return direct_text.strip()

    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) or []
        part_text = " ".join(
            part.text.strip()
            for part in parts
            if isinstance(getattr(part, "text", None), str) and part.text.strip()
        )
        if part_text:
            return part_text

    return ""


def generate_response(
    user_message: str,
    conversation_history: list = None,
    language: str = "en-US",
) -> str:
    if client is None:
        raise ValueError("GEMINI_API_KEY is missing from environment variables.")

    if conversation_history is None:
        conversation_history = []

    normalized_language = language if language in SUPPORTED_LANGUAGES else "en-US"
    system_prompt = _get_system_prompt(normalized_language)

    history_lines = []
    for turn in conversation_history:
        if not isinstance(turn, dict):
            continue
        role = str(turn.get("role", "")).lower()
        content = str(turn.get("content", "")).strip()
        if not content:
            continue
        speaker = "User" if role == "user" else "Echo"
        history_lines.append(f"{speaker}: {content}")

    history_lines.append(f"User: {user_message}")
    prompt = "\n".join(history_lines)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    assistant_message = _extract_text(response)
    if not assistant_message:
        assistant_message = FALLBACK_RESPONSE[normalized_language]

    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": assistant_message})

    return assistant_message


if __name__ == "__main__":
    print(generate_response("hi", []))
