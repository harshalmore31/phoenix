import pyttsx3
import whisper
import pyaudio
import wave
import os
from rich.console import Console
from pathlib import Path
import warnings

console = Console()

# Force FP32 to avoid FP16 warnings
os.environ["WHISPER_FP16"] = "0"

# Suppress FutureWarning from torch.load
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def record_audio(audio_path, duration=5):
    p = pyaudio.PyAudio()
    try:
        format_ = pyaudio.paInt16
        channels = 1
        rate = 16000
        chunk = 1024

        # Find a suitable input device
        device_index = next((i for i in range(p.get_device_count())
                             if p.get_device_info_by_index(i)['maxInputChannels'] > 0), None)
        if device_index is None:
            raise RuntimeError("No input device found")

        stream = p.open(format=format_,
                        channels=channels,
                        rate=rate,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=chunk)

        console.print("Recording...", style="bold yellow")
        frames = [stream.read(chunk, exception_on_overflow=False) for _ in range(int(rate / chunk * duration))]
        console.print("Finished recording.", style="bold green")

        # Save audio to file
        with wave.open(str(audio_path), 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format_))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def transcribe_audio():
    audio_path = Path("realtime_audio.wav")
    speak("I am listening. Please speak.")

    try:
        record_audio(audio_path, duration=5)
    except RuntimeError as e:
        console.print(f"Audio recording error: {e}", style="bold red")
        return "Audio recording failed."

    # Load Whisper model
    console.print("Loading Whisper model...", style="bold yellow")
    device = "cpu"  # Explicitly use CPU
    model = whisper.load_model("medium", device=device)

    # Transcribe audio
    console.print("Transcribing audio...", style="bold yellow")
    result = model.transcribe(str(audio_path))

    # Clean up the temporary audio file
    if audio_path.exists():
        audio_path.unlink()

    return result['text']

if __name__ == "__main__":
    result = transcribe_audio()
    console.print("\nTranscription result:", style="bold blue")
    console.print(result)
