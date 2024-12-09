import pyaudio
import wave
import requests
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("hugging_face_api_key")
# Whisper API Config
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": f"Bearer {api}"}


# Audio Config
CHUNK = 1024  # Record in chunks of 1024 samples
FORMAT = pyaudio.paInt16  # 16-bit audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate
THRESHOLD = 500  # Silence threshold (amplitude)
SILENCE_DURATION = 3  # Seconds of silence to stop recording

# Function to send audio file to Whisper API
def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            data = audio_file.read()
        response = requests.post(API_URL, headers=headers, data=data)

        if response.status_code != 200:
            return f"Error: {response.status_code}, {response.text}"
        
        transcription = response.json().get("text", "No transcription available.")
        return transcription

    except Exception as e:
        return f"Error: {str(e)}"

# Real-time recording with silence detection
def real_time_transcription_with_silence_detection():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening... Speak into the microphone.")
    print("Stop speaking to trigger transcription.")
    
    frames = []
    silent_chunks = 0  # Counter for silent chunks

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)

            # Convert audio data to numpy array for analysis
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitude = np.abs(audio_data).mean()

            if amplitude < THRESHOLD:
                silent_chunks += 1
            else:
                silent_chunks = 0  # Reset silence counter if sound detected

            # If silence detected for the specified duration, stop recording
            if silent_chunks > (SILENCE_DURATION * RATE / CHUNK):
                # Silence detected: Transcribing and cleanup
                print("Silence detected. Transcribing...")
                break

        # Save the audio in the current directory
        file_name = "recorded_audio.wav"
        file_path = os.path.join(os.getcwd(), file_name)
        
        wf = wave.open(file_path, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()

        # Send the audio to Whisper API
        transcription = transcribe_audio(file_path)
        return transcription

        # Keep the file if needed, or uncomment to delete it after processing
        # os.remove(file_path)

    except KeyboardInterrupt:
        print("\nStopped listening.")

    finally:
        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

# Run the transcription with silence detection
real_time_transcription_with_silence_detection()
