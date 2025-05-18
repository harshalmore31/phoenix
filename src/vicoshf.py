

import requests
from IPython.display import Audio

API_URL = "https://router.huggingface.co/fal-ai/fal-ai/dia-tts"
headers = {
    "Authorization": "Bearer ",  # Replace with your actual token
    "Accept": "audio/wav"  # Important: request audio format
}

def get_audio(text, output_path="output.wav"):
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": text},
        stream=True  # Get raw audio stream
    )
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return output_path

text = "[S1] Dia is an open weights text to dialogue model. [S2] You get full control over scripts and voices. [S1] Wow. Amazing. (laughs) [S2] Try it now on GitHub or Hugging Face."
audio_file = get_audio(text)

# Play it in Jupyter Notebook or IPython
Audio(audio_file)
