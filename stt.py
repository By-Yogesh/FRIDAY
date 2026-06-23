import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel
import config

# Load Whisper model once (this stays loaded, don't reload every time)
print("Loading Whisper model...")
model = WhisperModel(config.STT_MODEL_SIZE, device="cpu", compute_type="int8")
print("Whisper model loaded.")


def record_audio(filename="temp_audio.wav", duration=5, samplerate=16000):
    print(f"Recording for {duration} seconds... Speak now!")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    sf.write(filename, audio, samplerate)
    print("Recording finished.")
    return filename


def transcribe_audio(filename="temp_audio.wav"):
    segments, info = model.transcribe(filename, language="en")
    text = " ".join([segment.text for segment in segments])
    return text.strip()


def listen():
    audio_file = record_audio()
    text = transcribe_audio(audio_file)
    return text

from vad import record_with_vad

def listen_vad():
    audio_file = record_with_vad()
    text = transcribe_audio(audio_file)
    return text.strip()