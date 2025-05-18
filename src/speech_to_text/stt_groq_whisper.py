import time  # Importing time module for tracking execution time
import pyaudio
import wave
import os
import numpy as np
import threading
import groq
import pyttsx3
from dotenv import load_dotenv
import requests
import json
import simpleaudio as sa

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

import tempfile

load_dotenv()

# Ensure the GROQ_API_KEY environment variable is set
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")


# # --- Speak Function ---
# def speak(text: str):
#     """
#     Converts text to speech using Groq API (using a globally defined API key),
#     saves as WAV, and plays it in a background thread using simpleaudio.
#     """

#     # 2. Check if the global API key is defined and seems vali

#     # 3. Define API parameters (Using user-provided model/voice - double-check these with Groq docs)
#     url = "https://api.groq.com/openai/v1/audio/speech"
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "input": text,            # Text input
#         "model": "playai-tts",    # User-specified model (verify availability)
#         "voice": "Aaliyah-PlayAI",# User-specified voice (verify availability)
#         "response_format": "wav", # Output format
#         # "speed": 1.0            # Optional: Adjust speed
#     }

#     output_filename = None # Initialize filename variable

#     try:
#         # 4. Make the API Request
#         print("Requesting TTS from Groq API...")
#         response = requests.post(url, headers=headers, json=data, stream=True)
#         response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
#         print("API request successful.")

#         # 5. Save the audio stream to a temporary WAV file
#         # 'delete=False' is required because simpleaudio needs the path after 'with' closes the handle.
#         with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
#             output_filename = temp_file.name
#             audio_received = False
#             for chunk in response.iter_content(chunk_size=8192):
#                 if chunk: # Filter out potential empty chunks
#                     temp_file.write(chunk)
#                     audio_received = True

#             # Check if any audio data was actually written
#             if not audio_received:
#                  raise ValueError("Received empty audio stream from API (no chunks written).")

#         print(f"Audio saved temporarily to: {output_filename}")

#         # 6. Verify the temporary file isn't empty before trying to play
#         if os.path.getsize(output_filename) == 0:
#             print(f"Warning: Temporary audio file is empty ({output_filename}). Skipping playback.")
#             if os.path.exists(output_filename):
#                  try: os.remove(output_filename)
#                  except OSError: pass
#             return False

#         # 7. Define the playback and cleanup function for the thread
#         def play_audio_and_cleanup(filepath):
#             """Plays the audio file using simpleaudio and removes it afterwards."""
#             play_obj_instance = None # To hold the PlayObject for potential stop() call if needed
#             try:
#                 print(f"Attempting to load audio file: {filepath}")
#                 wave_obj = sa.WaveObject.from_wave_file(filepath)

#                 print(f"Playing audio via simpleaudio...")
#                 # Start playback (non-blocking call itself)
#                 play_obj_instance = wave_obj.play()
#                 # Wait for the playback to finish *within this thread*
#                 play_obj_instance.wait_done()
#                 print("Audio playback finished.")

#             except Exception as e:
#                 print(f"\nError during simpleaudio playback for {filepath}: {e}")
#                 print("Ensure the WAV file is valid and in a supported PCM format.")
#                 # If playback failed, we might still need to clean up
#             finally:
#                 # Always attempt to clean up the temporary file
#                 if os.path.exists(filepath):
#                     try:
#                         os.remove(filepath)
#                         print(f"Temporary audio file removed: {filepath}")
#                     except OSError as e:
#                         print(f"Error removing temporary file {filepath}: {e}")

#         # 8. Start playback in a background thread
#         print("Starting background audio playback thread...")
#         audio_thread = threading.Thread(target=play_audio_and_cleanup, args=(output_filename,))
#         audio_thread.daemon = True  # Allows main program to exit even if thread is running
#         audio_thread.start()

#         # 9. Return True immediately, indicating success in *starting* the process
#         return True

#     except requests.exceptions.RequestException as e:
#         print(f"API Request Failed: {e}")
#         if e.response is not None:
#             print(f"Status Code: {e.response.status_code}")
#             try: print(f"Response Body: {e.response.text}")
#             except Exception: print("(Could not decode response body)")
#         if output_filename and os.path.exists(output_filename):
#              try: os.remove(output_filename); print(f"Cleaned up partially created file: {output_filename}")
#              except OSError: pass
#         return False

#     except Exception as e:
#         print(f"An unexpected error occurred in speak function: {e}")
#         if output_filename and os.path.exists(output_filename):
#             try: os.remove(output_filename); print(f"Cleaned up temporary file due to error: {output_filename}")
#             except OSError: pass
#         return False


# Groq API Config
client = groq.Client(api_key=os.environ["GROQ_API_KEY"])
MODEL = "distil-whisper-large-v3-en"  # Model for transcription
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
    file_path = os.path.join("src", "backend", file_name)
    
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

# speak("Hello, this is a test of the text-to-speech conversion using the Groq API. Please let me know if you need any further assistance.")