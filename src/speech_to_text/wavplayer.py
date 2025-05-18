import os
import sys
import wave # Standard library module to read WAV properties

# --- Installation Check for simpleaudio ---
try:
    import simpleaudio as sa
except ImportError:
    print("Error: The 'simpleaudio' library is not installed.")
    print("Please install it by running: pip install simpleaudio")
    sys.exit(1)
except Exception as e:
    # Catches other potential import errors (like missing C dependencies on some systems)
    print(f"Error importing simpleaudio: {e}")
    print("Ensure you have necessary build tools if installation failed.")
    sys.exit(1)


# --- Function to Play WAV File using simpleaudio ---
def play_wav_simpleaudio(filepath):
    """
    Plays the WAV audio file using the simpleaudio library.

    Args:
        filepath (str): The full path to the .wav file.
    """
    # 1. Check if the file path exists
    if not os.path.exists(filepath):
        print(f"Error: File not found at path: {filepath}")
        return
    if not os.path.isfile(filepath):
        print(f"Error: Path exists but is not a file: {filepath}")
        return
    if not filepath.lower().endswith('.wav'):
        print(f"Warning: File does not have a .wav extension: {filepath}")
        # simpleaudio relies more strictly on WAV format

    # 2. Try to load and play the sound
    try:
        print(f"Attempting to load: {filepath} ...")
        # Load the WAV file
        wave_obj = sa.WaveObject.from_wave_file(filepath)

        print(f"Playing audio...")
        # Play the audio; play() returns a PlayObject
        # wait_done() blocks until playback finishes
        play_obj = wave_obj.play()
        play_obj.wait_done() 
        
        print("Playback finished.")

    except Exception as e:
        print(f"\nError playing sound with simpleaudio: {e}")
        # Add specific simpleaudio troubleshooting if needed
        print("Ensure the WAV file is valid and in a supported PCM format.")


# --- Main Execution Block ---
if __name__ == "__main__":
    wav_file_path = input("Enter the full path to the WAV audio file: ")
    wav_file_path = wav_file_path.strip(' \'"')

    # Call the function using simpleaudio
    play_wav_simpleaudio(wav_file_path)

    print("\nScript finished.")