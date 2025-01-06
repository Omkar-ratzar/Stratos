import os
import tkinter as tk
from PIL import Image, ImageTk  # Import PIL for image handling
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
    pygame.mixer.music.load(fpath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()

# Main processing function
def main_processing_function():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

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
        context1 = text + " Don't write anything other than command in output. The command is to be ran in CMD"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": context1}],
            model="llama-3.3-70b-versatile",
        )
        command = chat_completion.choices[0].message.content
        print(command)
        print(execute_command(command))

        explanation_text = text + execute_command(command) + " Explain the output and what just happened in 50 words or less"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": explanation_text}],
            model="llama-3.3-70b-versatile",
        )
        explanation = chat_completion.choices[0].message.content
        print(explanation)

        audio = generate(
            text=explanation,
            voice="Lily",
            api_key="sk_0d86ca6a5ca581587348fbedff77531fa3c4544fe4d1e547",
        )

        with open("output.wav", "wb") as f:
            f.write(audio)

        ding = 'ffmpeg -y -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)

        fpath = "foutput.wav"
        playwav(fpath)
    else:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": text}],
            model="llama-3.3-70b-versatile",
        )
        response = chat_completion.choices[0].message.content
        print(response)

        audio = generate(
            text=response,
            voice="Lily",
            api_key="sk_0d86ca6a5ca581587348fbedff77531fa3c4544fe4d1e547",
        )

        with open("output.wav", "wb") as f:
            f.write(audio)

        ding = 'ffmpeg -y -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)

        fpath = "foutput.wav"
        playwav(fpath)

# GUI Setup with an Image
def start_gui():
    root = tk.Tk()
    root.title("Floating Mic")
    root.attributes("-topmost", True)
    root.overrideredirect(True)  # Remove window borders and title bar

    # Load the imageimport os
    img_path = os.path.join(os.path.dirname(__file__), "img.png")
    img = Image.open(img_path)

    img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize image to fit window
    photo = ImageTk.PhotoImage(img)

    # Create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo  # Keep a reference to prevent garbage collection
    label.pack()

    # Make the label respond to clicks
    label.bind("<Button-1>", lambda event: main_processing_function())

    # Adjust window size to image dimensions
    window_width, window_height = img.size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = screen_height - window_height
    position_right = screen_width - window_width
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    root.mainloop()

# Start the GUI application
if __name__ == "__main__":
    start_gui()
