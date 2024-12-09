import requests
from pydub import AudioSegment
from pydub.playback import play

API_URL = "https://api-inference.huggingface.co/models/suno/bark"
headers = {"Authorization": "Bearer enter hf_apikey"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

audio_bytes = query({
    "inputs": "The answer to the universe is 42",
})

# Save the audio to a file
with open("output.wav", "wb") as f:
    f.write(audio_bytes)

# Load the audio file
audio = AudioSegment.from_wav("output.wav")

# Play the audio
play(audio)