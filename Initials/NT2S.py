from elevenlabs import voices, generate

import os

# List available voices
available_voices = voices()
print(available_voices)

# Generate and play audio
audio = generate(
    text="I just woke up dreaming about you",
    voice="Lily",
    api_key="API"
)
#Play the audio
with open("output.wav", "wb") as f:
    f.write(audio)

def execute_command(command):
    result = os.popen(command).read()
    return result
ding = 'ffmpeg -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
# To verify, print the variable
execute_command(ding)
from playsound import playsound
playsound("foutput.wav")
