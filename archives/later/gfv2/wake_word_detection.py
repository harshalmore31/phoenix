import time
import threading
import pvporcupine
import sounddevice as sd
import numpy as np
from concurrent.futures import ThreadPoolExecutor


def detect_wake_word(custom_ppn_path, access_key):
    """
    Detect wake word using Porcupine with multithreading for speed optimization.

    :param custom_ppn_path: Path to the custom wake word model (.ppn file)
    :param access_key: Picovoice access key
    :return: True if the wake word is detected
    """
    # Start timer for total execution time
    total_start_time = time.time()

    # Event flag to signal wake word detection
    detected = threading.Event()

    def audio_callback(indata, frames, time_info, status):
        """
        Callback function for real-time audio processing.
        """
        if status:
            print(f"Audio status error: {status}")
            return

        # Convert audio input from float32 to int16
        pcm = (indata[:, 0] * 32767).astype(np.int16)

        # Process audio to detect wake word
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            # print("Wake word detected!")
            detected.set()  # Signal wake word detection

    def listen_for_wake_word():
        """
        Function to listen for the wake word in a separate thread.
        """
        with sd.InputStream(
            samplerate=porcupine.sample_rate,
            channels=1,
            dtype="float32",
            callback=audio_callback,
            blocksize=porcupine.frame_length,
            latency="low"
        ):
            print("Listening for wake word...")
            while not detected.is_set():
                 start_time = time.time()
                 time.sleep(0.01)  # Base sleep time
                 elapsed_time = time.time() - start_time
                 time.sleep(max(0, 0.01 - elapsed_time))  # Adjust to maintain processing interval

    # Initialize Porcupine
    init_start_time = time.time()
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=[custom_ppn_path]
    )
    init_end_time = time.time()
    # print(f"Porcupine initialized in {init_end_time - init_start_time:.2f} seconds")

    try:
        # ThreadPoolExecutor to manage threading efficiently
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(listen_for_wake_word)
            detected.wait()  # Wait until wake word is detected
            # print("Wake word detected. Exiting listener thread.")
    finally:
        # Cleanup Porcupine
        cleanup_start_time = time.time()
        porcupine.delete()
        cleanup_end_time = time.time()
        # print(f"Cleanup completed in {cleanup_end_time - cleanup_start_time:.2f} seconds")

        # Total execution time
        total_end_time = time.time()
        # print(f"Total execution time: {total_end_time - total_start_time:.2f} seconds")

        return True  # Wake word detected
