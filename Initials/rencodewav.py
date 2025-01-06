from pydub import AudioSegment

# Load the audio
audio = AudioSegment.from_wav("natural.wav")

# Export the audio to a new WAV file (ensure proper format)
audio.export("naturalconverted.wav", format="wav")
