from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from elevenlabs import Voice, VoiceSettings, play
import os
from dotenv import load_dotenv

load_dotenv()

def spk(txt):
    client = ElevenLabs(
    api_key=os.getenv("eleven_labs_api"),
    )

    audio_stream = client.generate(
        text=txt,
        voice=Voice(
            voice_id='8J6BC8hEQXSzaJr7WMFn',
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            ),
        model="eleven_multilingual_v2",
        stream=True
    )

    stream(audio_stream)

# spk(txt="Hello, how is it going !")


