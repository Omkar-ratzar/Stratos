import os
import tkinter as tk
import speech_recognition as sr
from groq import Groq
from elevenlabs import voices, generate
import pyaudio
import pygame

client = Groq(api_key="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")

# Function to execute the command
def execute_command(command):
    result = os.popen(command).read()
    return result

# Play sound function
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
            api_key="sk_0d86ca6a5ca581587348fbedff77531fa3c4544fe4d1e547"
        )

        with open("output.wav", "wb") as f:
            f.write(audio)

        # Convert to proper format for playback
        ding = 'ffmpeg -y -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)

        fpath = "foutput.wav"
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
        from openai import OpenAI

        client = OpenAI()

        response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=response,
        )

        response.stream_to_file("output.wav")

        with open("output.wav", "wb") as f:
            f.write(audio)

        # Convert to proper format for playback
        ding = 'ffmpeg -y -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)

        fpath = "foutput.wav"
        playwav(fpath)

# GUI Setup
def start_gui():
    root = tk.Tk()
    root.title("Floating Mic")
    root.geometry("100x100")  # Fixed size window
    root.resizable(False, False)  # Disable resizing
    root.attributes("-topmost", True)  # Keep window always on top
    root.overrideredirect(True)  # Remove title bar and window borders

    # Position the window at the bottom-right of the screen
    window_width = 100
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = screen_height - window_height
    position_right = screen_width - window_width
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Button to start listening for commands
    listen_button = tk.Button(root, text="🎙️", command=main_processing_function, height=2, width=4)
    listen_button.pack(expand=True)

    # Start the GUI loop
    root.mainloop()

# Start the GUI application
if __name__ == "__main__":
    start_gui()
