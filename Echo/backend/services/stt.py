"""
STT Service using Deepgram SDK
Converts audio to text
"""
import os
from deepgram import DeepgramClient, PrerecordedOptions
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


def transcribe_audio(audio_bytes: bytes) -> str:
    try:
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        payload = {"buffer": audio_bytes}

        options = PrerecordedOptions(
            model="nova-2",
            language="multi",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(
            payload, options
        )

        transcript = response.results.channels[0].alternatives[0].transcript
        detected_language = response.results.channels[0].detected_language
        print(f"🌐 Detected language: {detected_language}")
        print(f"📝 Transcript: {transcript}")

        return transcript

    except Exception as e:
        print(f"❌ STT Error: {str(e)}")
        raise


if __name__ == "__main__":
    import os
    if os.path.exists("sample_audio.wav"):
        with open("sample_audio.wav", "rb") as f:
            transcribe_audio(f.read())
    else:
        print("Sample audio file not found. Create 'sample_audio.wav' to test.")
