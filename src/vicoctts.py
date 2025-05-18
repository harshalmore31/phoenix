import soundfile as sf
from dia.model import Dia
import simpleaudio as sa  # For playback

# Load the model
model = Dia.from_pretrained("nari-labs/Dia-1.6B")

# Input dialogue
text = "[S1] Dia is an open weights text to dialogue model. [S2] You get full control over scripts and voices. [S1] Wow. Amazing. (laughs) [S2] Try it now on GitHub or Hugging Face."

# Generate audio
output = model.generate(text)

# Save as proper WAV (not MP3!)
output_path = "simple.wav"
sf.write(output_path, output, 44100)

# Play it using simpleaudio
wave_obj = sa.WaveObject.from_wave_file(output_path)
play_obj = wave_obj.play()
play_obj.wait_done()
