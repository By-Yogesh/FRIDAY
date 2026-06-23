from stt import listen_vad
from router import route_command
from kokoro_onnx import Kokoro
import sounddevice as sd
import config
import keyboard
import time

print("Loading Friday's voice...")
kokoro = Kokoro(config.TTS_MODEL_PATH, config.TTS_VOICES_PATH)


def speak(text):
    samples, sample_rate = kokoro.create(
        text,
        voice=config.VOICE_NAME,
        speed=config.VOICE_SPEED,
        lang=config.VOICE_LANG
    )
    sd.play(samples, sample_rate)
    sd.wait()


print("Friday is ready.\n")
speak("Hey, I am Friday. I am online and ready to help.")


def main_loop():
    print("Press ctrl+Alt+Space to talk to Friday. Press Ctrl+C to exit.\n")

    while True:
        # Wait here until Alt+Space is pressed
        keyboard.wait("ctrl+alt+space")

        # Small pause so the keypress sound doesn't get picked up by mic
        time.sleep(0.3)

        text = listen_vad()
        print(f"You said: {text}")

        if not text.strip():
            speak("Sorry, I didn't catch that. Try again.")
            continue

        reply = route_command(text)
        print(f"Friday: {reply}")
        speak(reply)

        # Small gap before listening for next hotkey
        time.sleep(0.5)


if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nFriday going offline. Goodbye.")
        speak("Going offline. See you soon.")