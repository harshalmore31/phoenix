import os
import pyaudio
from wavify.wakeword import WakeWordEngine

# Initialize the Wake Word Engine
engine = WakeWordEngine("path/to/your/model", os.getenv("WAVIFY_API_KEY"))

# Function to record 5-second chunks of audio
def record_audio(chunk_duration=5, rate=16000, channels=1):
    """Record audio for the given duration and return as bytes."""
    audio_format = pyaudio.paInt16  # 16-bit format
    chunk_size = 1024  # Size of each audio buffer
    
    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size)
    
    print(f"Recording for {chunk_duration} seconds...")
    frames = []

    for _ in range(0, int(rate / chunk_size * chunk_duration)):
        data = stream.read(chunk_size)
        frames.append(data)
    
    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert frames to bytes
    return b''.join(frames)

# Main loop to continuously listen for the wake word
def listen_for_wake_word():
    print("Listening for the wake word...")
    while True:
        audio = record_audio(chunk_duration=5)
        
        # Pass the audio to the WakeWordEngine
        detection_probability = engine.detect(audio)
        print(f"Detection Probability: {detection_probability}")
        
        if detection_probability > 0.5:  # Threshold for detection
            print("Wake word detected!")
            break

if __name__ == "__main__":
    listen_for_wake_word()
