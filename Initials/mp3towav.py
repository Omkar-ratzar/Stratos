from pydub import AudioSegment

# Load MP3 file
mp3_file = "test1.mp3"
wav_file = "test2.wav"

# Convert MP3 to WAV
sound = AudioSegment.from_mp3(mp3_file)
sound.export(wav_file, format="wav")

print(f"Converted {mp3_file} to {wav_file}")
