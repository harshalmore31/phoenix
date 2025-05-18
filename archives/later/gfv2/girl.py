from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from elevenlabs import Voice, VoiceSettings, play


def spk(txt):
    client = ElevenLabs(
    api_key="sk_e50b16868713b6680edc29065247cb31d6bc0fd666018c38",
    )

    audio_stream = client.generate(
        text=txt,
        voice=Voice(
            voice_id='gHu9GtaHOXcSqFTK06ux',
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            ),
        model="eleven_multilingual_v2",
        stream=True
    )

    stream(audio_stream)

# spk(txt="Hello, how is it going !")


