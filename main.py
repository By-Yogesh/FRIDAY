import tkinter as tk
import threading
import time
import re
import keyboard
from kokoro_onnx import Kokoro
import sounddevice as sd
from stt import listen_vad
from router import route_command, NEEDS_LLM
from llm import ask_friday_stream
from ui import FridayUI
import config

ui = None
kk = None

# Sentence boundary — split on . ! ? followed by space or end
SENTENCE_END = re.compile(r'(?<![0-9])[.!?](?:\s|$)')


def handle_query(text):
    ui.add_message("you", text)
    ui.set_state("thinking")

    result = route_command(text)

    if result == NEEDS_LLM:
        speak_streaming(text)
    else:
        ui.add_message("friday", result)
        ui.set_state("speaking")
        speak_text(result)
        ui.set_state("idle")


def on_text_send(text):
    threading.Thread(target=handle_query, args=(text,), daemon=True).start()

    
def speak_text(text):
    """Speak a single chunk of text."""
    if not text.strip():
        return
    s, sr = kk.create(text.strip(),
                       voice=config.VOICE_NAME,
                       speed=config.VOICE_SPEED,
                       lang=config.VOICE_LANG)
    sd.play(s, sr)
    sd.wait()


def speak_streaming(user_text):
    """
    Stream LLM reply token by token.
    Speak each sentence the moment it's complete
    instead of waiting for the full reply.
    """
    buffer     = ""
    full_reply = ""
    first      = True

    for token in ask_friday_stream(user_text):
        buffer     += token
        full_reply += token

        match = SENTENCE_END.search(buffer)
        if match:
            sentence = buffer[:match.end()].strip()
            buffer   = buffer[match.end():]

            if len(sentence) > 4:
                if first:
                    ui.set_state("speaking")
                    first = False
                speak_text(sentence)

    # Speak anything left in buffer
    if buffer.strip() and len(buffer.strip()) > 2:
        ui.set_state("speaking")
        speak_text(buffer.strip())

    ui.add_message("friday", full_reply.strip())
    ui.set_state("idle")


def friday_loop():
    global kk
    ui.add_message("sys", "Loading Friday...")
    kk = Kokoro(config.TTS_MODEL_PATH, config.TTS_VOICES_PATH)
    ui.add_message("sys", "Friday is online.")
    ui.set_state("speaking")
    speak_text("Hey, I am Friday. I am online and ready to help.")
    ui.set_state("idle")

    while True:
        keyboard.wait("ctrl+alt+space")
        time.sleep(0.3)

        ui.set_state("listening")
        text = listen_vad()

        if not text.strip():
            ui.set_state("idle")
            speak_text("Sorry, I didn't catch that.")
            ui.set_state("idle")
            continue

        handle_query(text)
        time.sleep(0.5)


def main():
    global ui
    root = tk.Tk()
    ui = FridayUI(root)
    ui.set_text_callback(on_text_send)
    threading.Thread(target=friday_loop, daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    main()