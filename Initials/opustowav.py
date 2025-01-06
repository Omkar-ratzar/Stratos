from pydub import AudioSegment

# Path to your input OPUS file
input_opus_file = "stratos.opus"

# Path to save the converted WAV file
output_wav_file = "stratos.wav"

try:
    # Load the OPUS file
    audio = AudioSegment.from_file(input_opus_file, format="opus")

    # Export as WAV
    audio.export(output_wav_file, format="wav")
    print(f"File successfully converted to {output_wav_file}")

except Exception as e:
    print(f"An error occurred: {e}")
