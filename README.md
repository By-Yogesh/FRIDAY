# 🤖 FRIDAY — Local AI Voice Assistant

> *Inspired by Iron Man's F.R.I.D.A.Y. — built to run fully offline on a regular laptop.*

![Status](https://img.shields.io/badge/status-active--development-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🧠 What is FRIDAY?

FRIDAY is a lightweight, fully offline, voice-activated AI assistant that runs locally on your laptop — no cloud, no API keys, no internet required (after setup). You press a hotkey, speak a command or question, and FRIDAY listens, understands, responds in a human voice, and takes action on your machine.

This is an **ongoing personal project** — actively being built and improved. New features are added regularly.

---

## ✅ What FRIDAY Can Do Right Now

- 🎙️ Listen to your voice using smart VAD (Voice Activity Detection)
- 🧏 Convert your speech to text (Whisper STT)
- 🧠 Understand your query using a local LLM (Qwen2.5)
- 🗣️ Respond in a natural human voice (Kokoro TTS)
- 💻 Open apps — VS Code, Notepad, Calculator, Chrome
- 🌐 Open Google, search anything on Google
- 🚀 "Initialize my setup" — opens VS Code + all your profile tabs in Chrome in one command
- 💬 Have a casual conversation like a real human friend (not robotic!)

---

## 🛠️ Tech Stack

| Layer | Tool | Description |
|---|---|---|
| Voice Activity Detection | `webrtcvad` | Detects when you start and stop speaking |
| Speech to Text | `faster-whisper` (tiny, int8) | Converts your voice to text, runs on CPU |
| Language Model | `Qwen2.5:3b` via Ollama | The brain — understands and replies |
| Text to Speech | `kokoro-onnx` (int8) | Natural human-sounding voice, runs locally |
| Actions | Python `subprocess` + `webbrowser` | Opens apps and URLs |
| Trigger | `keyboard` hotkey (`Ctrl+Alt+Space`) | Wake FRIDAY from anywhere on your laptop |

---

## 📁 Project Structure

```
FRIDAY/
│
├── main.py               ← Entry point — runs the full assistant loop
├── config.py             ← All settings: voice, model, URLs, personality
│
├── vad.py                ← Mic listening + smart speech detection
├── stt.py                ← Voice → Text (faster-whisper)
├── llm.py                ← Text → Qwen → Reply
├── tts.py                ← Reply → Kokoro → Spoken voice
├── router.py             ← Decides: is this a command or a question?
│
├── actions/
│   ├── __init__.py
│   ├── apps.py           ← Open VS Code, Notepad, Calculator, Chrome
│   ├── browser.py        ← Open URLs, Google Search
│   └── init_setup.py     ← "Initialize my setup" routine
│
├── kokoro-v1.0.int8.onnx ← Kokoro voice model (download separately)
└── voices-v1.0.bin       ← Kokoro voice data (download separately)
```

---

## 🚀 How to Run (Quick Start)

```bash
# 1. Activate virtual environment
friday_env\Scripts\activate

# 2. Make sure Ollama is running (in a separate terminal)
ollama serve

# 3. Start FRIDAY
python main.py
```

Press `Ctrl+Alt+Space` from anywhere on your laptop to talk to FRIDAY.

> 📖 For full setup instructions from scratch, see [HOW_TO_USE.md](HOW_TO_USE.md)

---

## 🗺️ Roadmap — What's Coming Next

- [ ] Phase 3: Testing, optimization, and personality polish
- [ ] Error handling (mic failure, Ollama offline, empty audio)
- [ ] More voice commands (play music, tell time, system stats)
- [ ] Screen reader — FRIDAY can see what's on your screen
- [ ] Camera integration — face detection, presence awareness
- [ ] Memory — FRIDAY remembers things you tell it across sessions
- [ ] Full system control — control mouse, keyboard, files by voice

---

## ⚙️ System Requirements

| Component | Minimum | Tested On |
|---|---|---|
| CPU | Any modern x86 CPU | Ryzen 5 3500U |
| RAM | 8GB | 8GB DDR4 |
| Storage | 5GB free | 500GB SSD |
| OS | Windows 10/11 | Windows 11 |
| Python | 3.10+ | 3.10.10 |
| Internet | Only for initial setup | — |

---

## 👤 Author

**Yogesh** — AI/ML Student | Building FRIDAY as a learning project in AI, local LLMs, and voice systems.

> 🚧 This project is actively under development. Features are being added regularly. Feel free to fork, star, or follow along.

---

## 📄 License

MIT License — free to use, modify, and share.
