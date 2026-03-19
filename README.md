<div align="center">

# Echo
### *Your calm AI talk buddy*

![Echo](https://img.shields.io/badge/Echo-Voice%20AI-F59E0B?style=for-the-badge&labelColor=0F0F0F)
![Next.js](https://img.shields.io/badge/Next.js-15-white?style=for-the-badge&logo=nextdotjs&labelColor=0F0F0F)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&labelColor=0F0F0F)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?style=for-the-badge&logo=google&labelColor=0F0F0F)
![Murf AI](https://img.shields.io/badge/Murf%20AI-TTS-F59E0B?style=for-the-badge&labelColor=0F0F0F)

**A real-time voice-to-voice AI companion built for people with social anxiety and introverts.**  
*No typing. No judgment. Just speak — Echo listens.*

---

[**Live Demo**](#) · [**Report Bug**](#) · [**Request Feature**](#)

</div>

---

## 📖 About Echo

Most AI tools make you type. Echo makes you talk.

Echo is a voice-to-voice AI companion designed as a **safe, judgment-free space** for people with social anxiety and introverts. Speak naturally in English, Tamil, or Hindi — Echo automatically detects your language, understands your context, and responds with a warm, human-like voice in real time.

Built at the **Murf AI Hackathon 2025**, Echo uses a seamless pipeline:  
`Your Voice → Speech-to-Text → Gemini 2.5 Flash → Murf AI TTS → Echo's Voice`

---

## ✨ Features

- 🎙 **Voice-First** — No keyboard required. Just click and speak
- 🌐 **Auto Language Detection** — Detects English, Tamil & Hindi automatically mid-conversation
- 😌 **Zero Judgment** — Warm, calm responses designed for anxious and introverted users
- ⚡ **Real-Time Pipeline** — Full STT → AI → TTS loop in under 2 seconds
- 🎬 **Cinematic UI** — Ambient orb that breathes, ripples, and reacts to every state
- 💬 **Live Transcript** — Chat bubbles show the conversation as it happens
- 🔴 **Connection Status** — Always know when Echo is ready

---

## 🧠 How It Works

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  You Speak  │────▶│  Web Speech │────▶│  Gemini 2.5 Flash│────▶│  Murf AI    │
│  (Browser)  │     │  API (STT)  │     │  (AI Response)   │     │  TTS Voice  │
└─────────────┘     └─────────────┘     └──────────────────┘     └─────────────┘
```

1. **You speak** — Browser captures audio via Web Speech API
2. **STT** — Speech is transcribed to text in real time
3. **Gemini 2.5 Flash** — Detects your language, understands context, generates a warm reply
4. **Murf AI TTS** — Response is converted to natural human voice and played back

---

## 🎨 UI States

Echo's orb reacts intelligently to every moment:

| State | Visual | Behavior |
|-------|--------|----------|
| 💤 **Idle** | Subtle cyan/amber breathing glow | Calm, waiting |
| 🎤 **Listening** | Ripple rings expand from orb | Orange glow activates |
| 🧠 **Thinking** | Slight dimming | Minimal movement |
| 🗣 **Speaking** | Audio visualizer bars | Glow reacts to voice |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 (React) |
| Backend | Python (FastAPI / Flask) |
| AI Brain | Gemini 2.5 Flash |
| Text-to-Speech | Murf AI API |
| Speech-to-Text | Web Speech API (Browser Native) |
| Code Assist | GitHub Copilot |

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- Gemini API Key ([Get one here](https://aistudio.google.com))
- Murf AI API Key ([Get one here](https://murf.ai))

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/echo-ai.git
cd echo-ai
```

**2. Setup the frontend**
```bash
cd frontend
npm install
```

**3. Setup the backend**
```bash
cd backend
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the `backend` folder:
```env
GEMINI_API_KEY=your_gemini_api_key_here
MURF_API_KEY=your_murf_api_key_here
```

Create a `.env.local` file in the `frontend` folder:
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

**5. Run the backend**
```bash
cd backend
python main.py
```

**6. Run the frontend**
```bash
cd frontend
npm run dev
```

**7. Open your browser**
```
http://localhost:3000
```

---

## 📁 Project Structure

```
echo-ai/
├── frontend/                  # Next.js app
│   ├── app/
│   │   ├── page.tsx           # Main Echo interface
│   │   └── layout.tsx
│   ├── public/
│   └── package.json
│
├── backend/                   # Python server
│   ├── main.py                # Entry point
│   ├── routes/
│   │   └── chat.py            # STT → Gemini → Murf pipeline
│   ├── services/
│   │   ├── gemini.py          # Gemini API integration
│   │   └── murf.py            # Murf AI TTS integration
│   └── requirements.txt
│
└── README.md
```

---

## 🌐 Supported Languages

| Language | Code | Auto-Detection |
|----------|------|----------------|
| English | `en` | ✅ |
| Tamil | `ta` | ✅ |
| Hindi | `hi` | ✅ |

Echo detects the language from the transcribed text automatically — no manual selection needed. Switch languages mid-conversation and Echo adapts instantly.

---

## 🤖 System Prompt Philosophy

Echo is designed to feel like a **calm, warm friend** — not a formal assistant. Key principles:

- Responds in the same language the user speaks
- Keeps replies short and conversational (2-4 sentences)
- Never uses markdown, bullet points, or lists in responses
- Adapts tone to match user's emotional state
- Ends with a natural follow-up to keep conversation flowing

---

## 🏆 Built At

**Murf AI Hackathon 2025**  
Features used: Text-to-Speech · API Integration · Real-time Voice Generation

---

## 🙏 Acknowledgements

- [Murf AI](https://murf.ai) — for the incredibly natural TTS voices
- [Google Gemini](https://deepmind.google/technologies/gemini/) — for the AI brain
- [Next.js](https://nextjs.org) — for the frontend framework
- [GitHub Copilot](https://github.com/features/copilot) — for code assistance

---

<div align="center">

**E c h o · Here to listen.**

*Built for everyone who finds it easier to be heard than to be seen.*

</div>
