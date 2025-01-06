import os
from groq import Groq
import speech_recognition as sr
from elevenlabs import voices, generate
import pyaudio
import pygame
client = Groq(api_key="API")

# Function to execute the command
def execute_command(command):
    result = os.popen(command).read()
    return result

#play sound function
def playwav(fpath):
    pygame.mixer.init()

    # Load and play the audio
    pygame.mixer.music.load(fpath)
    pygame.mixer.music.play()

    # Wait until playback is done
    while pygame.mixer.music.get_busy():
        continue

    # Stop the mixer
    pygame.mixer.quit()


# Main processing function
def main_processing_function():
    # Step 1: Speech to Text (Live Input)
    recognizer = sr.Recognizer()

    # Start listening to microphone
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Listening...")
        audio = recognizer.listen(source)  # Listen to the microphone input

    try:
        text = recognizer.recognize_google(audio)
        print("Converted text:", text)
    except sr.UnknownValueError:
        print("Speech not understood")
        return
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return

    # Step 2: Processing based on the text
    if "stratos" in text:
        # Command processing block
        context1 = text + " Don't write anything other than command in output. The command is to be ran in CMD"
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": context1}
            ],
            model="llama-3.3-70b-versatile",
        )

        command = chat_completion.choices[0].message.content
        print(command)
        print(execute_command(command))

        # Explaining the command
        explanation_text = text + execute_command(command) + " Explain the output and what just happened in 50 words or less"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": explanation_text}],
            model="llama-3.3-70b-versatile",
        )

        explanation = chat_completion.choices[0].message.content
        print(explanation)

        # Generate and play explanation audio
        audio = generate(
            text=explanation,
            voice="Lily",
            api_key="API"
        )

        with open("output.wav", "wb") as f:
            f.write(audio)

        # Convert to proper format for playback
        ding = 'ffmpeg -y -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)

        fpath="foutput.wav"
        playwav(fpath)

    else:
        # Handling other cases
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": text}
            ],
            model="llama-3.3-70b-versatile",
        )

        response = chat_completion.choices[0].message.content
        print(response)

        # Generate and play the response audio
        audio = generate(
            text=response,
            voice="Lily",
            api_key="API"
        )

        with open("output.wav", "wb") as f:
            f.write(audio)

        # Convert to proper format for playback
        ding = 'ffmpeg -y -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)


        fpath="foutput.wav"
        playwav(fpath)

while(True):
    main_processing_function()
