from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from elevenlabs import Voice, VoiceSettings, play


def spk(txt):
    client = ElevenLabs(
    api_key="sk_47011ebb91913053956986afc19fcfb623696109ef8bc019",
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


