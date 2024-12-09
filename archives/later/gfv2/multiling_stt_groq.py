import time  # Importing time module for tracking execution time
import pyaudio
import wave
import os
import numpy as np
import threading
import groq
import pyttsx3
from dotenv import load_dotenv

load_dotenv()

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Select the female voice (Microsoft Zira)
    for voice in voices:
        if "Zira" in voice.name:
            engine.setProperty('voice', voice.id)
            break
    else:
        print("Female voice not found. Using default voice.")
    
    engine.say(text)
    engine.runAndWait()

# Groq API Config
client = groq.Client(api_key=os.environ["GROQ_API_KEY"])
MODEL = "whisper-large-v3"  # Model for transcription
LANGUAGE = "en"  # Language for transcription
TEMPERATURE = 0.0  # Temperature for decoding

# Audio Config
CHUNK = 1024  # Record in chunks of 1024 samples
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate
THRESHOLD = 500  # Silence threshold (amplitude)
SILENCE_DURATION = 2.7  # Seconds of silence to stop recording


# Function to send audio file to Groq API
def transcribe_audio(file_path):
    start_time = time.time()  # Start timer
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(file_path, audio_file.read()),
                model=MODEL,
                language=LANGUAGE,
                temperature=TEMPERATURE,
                response_format="json"
            )
        print(f"Transcription: {transcription.text}")
        return transcription.text

    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"
    finally:
        end_time = time.time()  # End timer
        # print(f"Time for transcription: {end_time - start_time:.2f} seconds")


# Real-time recording with silence detection
def record_audio(frames, stream, silence_event):
    start_time = time.time()  # Start timer for recording
    silent_chunks = 0  # Counter for silent chunks
    print("Listening... Speak into the microphone.")
    # print("Stop speaking to trigger transcription.")
    
    while not silence_event.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

        # Convert audio data to numpy array for analysis
        audio_data = np.frombuffer(data, dtype=np.int16)
        amplitude = np.abs(audio_data).mean()

        if amplitude < THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0  # Reset silence counter if sound detected

        # If silence detected for the specified duration, signal to stop recording
        if silent_chunks > (SILENCE_DURATION * RATE / CHUNK):
            print("Silence detected. Transcribing...")
            silence_event.set()
    end_time = time.time()  # End timer for recording
    # print(f"Time for recording: {end_time - start_time:.2f} seconds")


def save_and_transcribe(frames, p):
    # Save the audio in the current directory
    start_time = time.time()  # Start timer for saving audio
    file_name = "recorded_audio.wav"
    file_path = os.path.join(os.getcwd(), file_name)
    
    wf = wave.open(file_path, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    end_time = time.time()  # End timer for saving audio
    # print(f"Time for saving audio: {end_time - start_time:.2f} seconds")

    # Send the audio to Groq API
    return transcribe_audio(file_path)


def real_time_transcription_with_threads():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    silence_event = threading.Event()

    try:
        # Start audio recording thread
        record_thread = threading.Thread(target=record_audio, args=(frames, stream, silence_event))
        record_thread.start()

        # Wait for recording to complete
        record_thread.join()

        # Save and transcribe audio in the main thread
        transcription = save_and_transcribe(frames, p)
        return transcription

    except KeyboardInterrupt:
        print("\nStopped listening.")

    finally:
        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

# real_time_transcription_with_threads()