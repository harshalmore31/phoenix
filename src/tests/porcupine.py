import time  # Importing time module for tracking execution time
import pvporcupine
import sounddevice as sd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

def audio_callback(indata, frames, time, status):
    """
    Callback function to process audio chunks.
    """
    if status:
        print(f"Audio status error: {status}")
    # Convert audio input from float32 to int16
    pcm = (indata[:, 0] * 32767).astype(np.int16)
    keyword_index = porcupine.process(pcm)
    if keyword_index >= 0:
        print("Wake word detected!")
        global detected
        detected = True  # Signal the loop to stop

# Corrected path with raw string or double backslashes
custom_ppn_path = r"assests\wake_word_detect\Phoenix_en_windows_v3_0_0.ppn"

# Initialize Porcupine and track initialization time
start_init_time = time.time()
porcupine = pvporcupine.create(
    access_key=os.getenv("picovoice_api_key"),  # Replace with your Picovoice Access Key
    keyword_paths=[custom_ppn_path]
)
end_init_time = time.time()
print(f"Porcupine initialization time: {end_init_time - start_init_time:.2f} seconds")

# Flag to control the audio stream loop
detected = False

try:
    # Start listening and track listening duration
    start_listen_time = time.time()
    with sd.InputStream(
        samplerate=porcupine.sample_rate,
        channels=1,
        dtype="float32",  # Ensure the audio data is float32
        callback=audio_callback,
        blocksize=porcupine.frame_length
    ):
        print("Listening for the wake word...")
        while not detected:
            pass  # Keep the stream running until wake word is detected
    end_listen_time = time.time()
    print(f"Time spent listening for wake word: {end_listen_time - start_listen_time:.2f} seconds")
finally:
    porcupine.delete()
    print("Wake word detected. Stopping...")
