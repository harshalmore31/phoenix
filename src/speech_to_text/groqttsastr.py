import os
import sys
import requests
from dotenv import load_dotenv

try:
    import simpleaudio as sa
except ImportError:
    sys.exit("Error: Install 'simpleaudio' with `pip install simpleaudio`.")

def speak(text: str):
    """
    Converts text to speech using GROQ API and plays it. Blocks until playback finishes.
    """
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY not set in environment variables.")

    url = "https://api.groq.com/openai/v1/audio/speech"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "playai-tts",
        "voice": "Arista-PlayAI",
        "input": text,
        "response_format": "wav"
    }

    output_file = "out.wav"

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return
    except Exception as e:
        print(f"Error saving audio: {e}")
        return

    try:
        wave_obj = sa.WaveObject.from_wave_file(output_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # This line ensures it BLOCKS until playback is complete
    except Exception as e:
        print(f"Playback failed: {e}")
