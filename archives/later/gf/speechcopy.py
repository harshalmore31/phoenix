import pyttsx3
import whisper
import pyaudio
import wave
import os
import torch
from rich.console import Console
from pathlib import Path
import numpy as np
import time

console = Console()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def calculate_rms(data):
    """Calculate RMS value from raw audio data"""
    samples = np.frombuffer(data, dtype=np.int16)
    rms = np.sqrt(np.mean(samples**2))
    return rms

def record_audio(audio_path, silence_threshold=500, silence_duration=3):
    p = pyaudio.PyAudio()
    try:
        format_ = pyaudio.paInt16
        channels = 1
        rate = 16000
        chunk = 1024

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

        console.print("Recording... Speak now.", style="bold yellow")
        frames = []

        silence_start = None

        while True:
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)

            # Calculate RMS to check silence
            rms = calculate_rms(data)
            if rms < silence_threshold:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > silence_duration:
                    console.print("Silence detected for 3 seconds. Stopping recording.", style="bold green")
                    break
            else:
                silence_start = None

        console.print("Finished recording.", style="bold green")

        with wave.open(str(audio_path), 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format_))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

class SafeWhisperLoader:
    @staticmethod
    def safe_load_model():
        """Safely load the Whisper model with proper configurations"""
        console.print("Loading Whisper model...", style="bold yellow")

        # Override torch.load to use weights_only=True
        original_load = torch.load
        try:
            def safe_load(*args, **kwargs):
                kwargs['weights_only'] = True
                return original_load(*args, **kwargs)

            torch.load = safe_load

            # Load model with FP32 precision for CPU
            model = whisper.load_model("small")
            model = model.float()  # Ensure FP32 precision

            return model

        finally:
            # Restore original torch.load
            torch.load = original_load

def transcribe_audio():
    audio_path = Path("realtime_audio.wav")
    print("I am listening. Speak now.")

    try:
        record_audio(audio_path)
    except RuntimeError as e:
        console.print(f"Audio recording error: {e}", style="bold red")
        return "Audio recording failed."

    try:
        # Load model with safe configurations
        model = SafeWhisperLoader.safe_load_model()

        # Transcribe audio
        console.print("Transcribing audio...", style="bold yellow")
        result = model.transcribe(str(audio_path), fp16=False)  # Explicitly disable FP16
        return result['text']

    except Exception as e:
        console.print(f"Transcription error: {e}", style="bold red")
        return "Transcription failed."

    finally:
        if audio_path.exists():
            audio_path.unlink()

if __name__ == "__main__":
    # Configure torch for better CPU performance
    torch.set_num_threads(torch.get_num_threads())

    # Set environment variables to ensure FP32 usage
    os.environ["WHISPER_USE_FP16"] = "FALSE"

    result = transcribe_audio()
    console.print("\nTranscription result:", style="bold blue")
    console.print(result)
