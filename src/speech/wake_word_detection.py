import pvporcupine
import sounddevice as sd
import numpy as np

def detect_wake_word(custom_ppn_path, access_key):
    """
    Function to detect the wake word using Porcupine's custom model.

    :param custom_ppn_path: Path to the custom wake word model (.ppn file)
    :param access_key: Picovoice access key
    :return: None
    """
    
    # Flag to control the audio stream loop
    detected = False

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

    # Initialize Porcupine
    porcupine = pvporcupine.create(
        access_key=access_key,  # Picovoice Access Key
        keyword_paths=[custom_ppn_path]
    )

    try:
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
    finally:
        porcupine.delete()
        return 1
