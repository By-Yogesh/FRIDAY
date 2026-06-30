import customtkinter as ctk
import psutil
import threading
import time
import re
import queue
import keyboard
from kokoro_onnx import Kokoro
import sounddevice as sd
from stt import listen_vad
from router import route_command, NEEDS_LLM
from llm import ask_friday_stream
from ui import FridayUI
from weather import get_weather
import cv2
from PIL import Image, ImageTk
from camera import Camera
import config


ui = None
kk = None
session_start  = time.time()
command_count  = 0
camera = Camera()
camera_running = False

SENTENCE_END = re.compile(r'(?<![0-9])[.!?](?:\s|$)')


def update_system_stats():
    cpu_pct = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("D:\\")  # change to "C:\\" if Friday is on C drive

    ui.update_stats(
        cpu_pct=cpu_pct,
        ram_pct=mem.percent,
        ram_used_gb=mem.used / (1024 ** 3),
        ram_total_gb=mem.total / (1024 ** 3),
        disk_used_gb=disk.used / (1024 ** 3),
        disk_total_gb=disk.total / (1024 ** 3),
    )

    ui.root.after(2000, update_system_stats)  # refresh every 2 seconds

def update_uptime():
    boot_time = psutil.boot_time()
    elapsed = int(time.time() - boot_time)

    h = elapsed // 3600
    m = (elapsed % 3600) // 60
    s = elapsed % 60
    uptime_str = f"{h:02d}:{m:02d}:{s:02d}"

    load_pct = psutil.cpu_percent(interval=None)

    ui.update_uptime(uptime_str, command_count, load_pct)
    ui.root.after(1000, update_uptime)

def update_weather_loop():
    data = get_weather()
    if data:
        ui.update_weather(
            temp=data["temp"],
            feels_like=data["feels_like"],
            humidity=data["humidity"],
            wind=data["wind"],
            condition=data["condition"],
            city=data["city"]
        )
    else:
        ui.add_message("sys", "Weather unavailable — check API key or internet connection.")

    ui.root.after(600000, update_weather_loop)   # refresh every 10 minutes

def on_camera_toggle():
    global camera_running
    if not camera_running:
        ok = camera.start()
        if not ok:
            ui.add_message("sys", "Could not access camera. Check it's connected and not used by another app.")
            return
        camera_running = True
        ui.set_camera_state(True)
        camera_loop()
    else:
        camera_running = False
        camera.stop()
        ui.set_camera_state(False)


def camera_loop():
    if not camera_running:
        return
    frame = camera.get_frame()
    if frame is not None:
        frame = cv2.resize(frame, (260, 140))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image=img)
        ui.update_camera_frame(photo)
    ui.root.after(100, camera_loop)   # ~10 fps, light on CPU

def play_with_typing(text, samples, sample_rate):
    """
    Plays audio while revealing the text word-by-word at roughly
    the same pace as the speech, giving a live 'typing' effect.
    """
    duration = len(samples) / sample_rate
    words = text.split()

    sd.play(samples, sample_rate)

    if words:
        delay = duration / len(words)
        for w in words:
            ui.append_text(w + " ")
            time.sleep(delay)

    sd.wait()


def speak_full(text):
    """For instant command replies (open notepad, etc.) — not streamed."""
    ui.start_message("friday")
    ui.set_state("speaking")
    samples, sr = kk.create(text, voice=config.VOICE_NAME,
                             speed=config.VOICE_SPEED, lang=config.VOICE_LANG)
    play_with_typing(text, samples, sr)
    ui.end_message()
    ui.set_state("idle")


def speak_streaming(user_text):
    """
    Overlaps LLM generation, TTS synthesis, and playback using two
    background threads, so the next sentence is ready before the
    current one finishes playing. Removes the silent gap between
    sentences that caused the buffering/stutter.
    """
    sentence_q = queue.Queue()
    audio_q    = queue.Queue()

    def llm_producer():
        buffer = ""
        for token in ask_friday_stream(user_text):
            buffer += token
            match = SENTENCE_END.search(buffer)
            if match:
                sentence = buffer[:match.end()].strip()
                buffer = buffer[match.end():]
                if len(sentence) > 4:
                    sentence_q.put(sentence)
        if buffer.strip():
            sentence_q.put(buffer.strip())
        sentence_q.put(None)

    def tts_producer():
        while True:
            sentence = sentence_q.get()
            if sentence is None:
                audio_q.put(None)
                break
            samples, sr = kk.create(sentence, voice=config.VOICE_NAME,
                                     speed=config.VOICE_SPEED, lang=config.VOICE_LANG)
            audio_q.put((sentence, samples, sr))

    threading.Thread(target=llm_producer, daemon=True).start()
    threading.Thread(target=tts_producer, daemon=True).start()

    ui.start_message("friday")
    first = True

    while True:
        item = audio_q.get()
        if item is None:
            break
        sentence, samples, sr = item
        if first:
            ui.set_state("speaking")
            first = False
        play_with_typing(sentence + " ", samples, sr)

    ui.end_message()
    ui.set_state("idle")


def handle_query(text):

    global command_count
    command_count += 1

    ui.add_message("you", text)
    ui.set_state("thinking")

    result = route_command(text)

    if result == NEEDS_LLM:
        speak_streaming(text)
    else:
        speak_full(result)


def on_text_send(text):
    threading.Thread(target=handle_query, args=(text,), daemon=True).start()


def friday_loop():
    global kk
    ui.add_message("sys", "Loading Friday...")
    kk = Kokoro(config.TTS_MODEL_PATH, config.TTS_VOICES_PATH)
    ui.add_message("sys", "Friday is online.")
    speak_full("Hey, I am Friday. I am online and ready to help.")

    while True:
        keyboard.wait("ctrl+alt+space")
        time.sleep(0.3)

        ui.set_state("listening")
        text = listen_vad()

        if not text.strip():
            ui.set_state("idle")
            speak_full("Sorry, I didn't catch that.")
            continue

        handle_query(text)
        time.sleep(0.5)


def main():
    global ui
    root = ctk.CTk()
    ui = FridayUI(root)
    ui.set_text_callback(on_text_send)
    ui.set_camera_toggle_callback(on_camera_toggle)
    threading.Thread(target=friday_loop, daemon=True).start()
    ui.root.after(1000, update_system_stats)
    ui.root.after(1000, update_uptime)
    ui.root.after(2000, update_weather_loop)
    root.mainloop()


if __name__ == "__main__":
    main()