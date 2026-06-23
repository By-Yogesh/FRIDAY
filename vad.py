import pyaudio
import webrtcvad
import wave

SAMPLE_RATE = 16000
FRAME_DURATION_MS = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)
SILENCE_LIMIT_MS = 1000          # stop after 1 sec of silence (was 800)
SILENCE_FRAMES = SILENCE_LIMIT_MS // FRAME_DURATION_MS
TRIGGER_FRAMES = 3               # need 3 consecutive speech frames to confirm real speech
MAX_RECORD_SECONDS = 12

vad = webrtcvad.Vad(3)  # most strict mode


def record_with_vad(filename="temp_audio.wav"):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE,
                         input=True, frames_per_buffer=FRAME_SIZE)

    print("Listening... speak whenever you're ready")

    frames = []
    triggered = False
    silence_count = 0
    speech_confirm_count = 0
    pre_buffer = []  # holds last few frames before trigger, so we don't cut off the start of your word
    max_frames = int(MAX_RECORD_SECONDS * 1000 / FRAME_DURATION_MS)
    frame_count = 0

    while frame_count < max_frames:
        frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
        is_speech = vad.is_speech(frame, SAMPLE_RATE)
        frame_count += 1

        if not triggered:
            pre_buffer.append(frame)
            if len(pre_buffer) > TRIGGER_FRAMES:
                pre_buffer.pop(0)

            if is_speech:
                speech_confirm_count += 1
                if speech_confirm_count >= TRIGGER_FRAMES:
                    triggered = True
                    frames.extend(pre_buffer)  # include the few frames right before trigger
                    print("Speech detected, recording...")
            else:
                speech_confirm_count = 0
        else:
            frames.append(frame)
            if not is_speech:
                silence_count += 1
                if silence_count > SILENCE_FRAMES:
                    break
            else:
                silence_count = 0

    print("Done listening.")
    sample_width = audio.get_sample_size(pyaudio.paInt16)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename