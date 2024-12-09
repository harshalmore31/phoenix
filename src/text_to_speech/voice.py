from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs

def spk(txt):
    client = ElevenLabs(
    api_key="sk_47011ebb91913053956986afc19fcfb623696109ef8bc019", # Defaults to ELEVEN_API_KEY
    )

    # audio = client.generate(
    #     text=txt,
    #     voice=Voice(
    #         voice_id='UgBBYS2sOqTuMpoF3BR0',
    #         settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
    #     )
    # )
    # play(audio)

    audio_stream = client.text_to_speech.convert_as_stream(
        text=txt,
        # voice_id='UgBBYS2sOqTuMpoF3BR0', Mark
        voice_id="8J6BC8hEQXSzaJr7WMFn",
        enable_logging="0",
        optimize_streaming_latency=0,
        output_format="mp3_22050_32",
    )

    play(audio_stream)

# spk(txt="Hello, how is it going !")


