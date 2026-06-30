# ===== FRIDAY CONFIG =====

# --- Voice Settings (TTS) ---
TTS_MODEL_PATH = "kokoro-v1.0.int8.onnx"
TTS_VOICES_PATH = "voices-v1.0.bin"
VOICE_NAME = "af_jessica"
VOICE_SPEED = 1.0
VOICE_LANG = "en-us"

# --- LLM Settings ---
LLM_MODEL = "qwen2.5:3b"
LLM_NUM_CTX = 2048
LLM_NUM_THREAD = 5

# --- STT Settings ---
STT_MODEL_SIZE = "tiny"

# --- Friday's Personality ---
SYSTEM_PROMPT = """You are Friday, a personal AI assistant.
Talk like a smart close friend — casual, warm, direct.
Never say "Certainly!" or "Of course!" or sound robotic.
Keep replies short unless asked for detail.
Reply in 1-3 sentences max for casual questions.
"""