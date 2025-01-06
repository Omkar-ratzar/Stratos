import os
import tkinter as tk
from PIL import Image, ImageTk  # Import PIL for image handling
import speech_recognition as sr
from groq import Groq
from elevenlabs import voices, generate
import pyaudio
import pygame



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















client = Groq(api_key="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")
# Main processing function
def main_processing_function(text=None):
    recognizer = sr.Recognizer()

    if text:  # If text is provided manually
        processed_text = text
    else:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            processed_text = recognizer.recognize_google(audio)
            print("Converted text:", processed_text)
        except sr.UnknownValueError:
            print("Speech not understood")
            return
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return

    # Process the text (same logic as before)
    if "stratos" in processed_text:
        context1 = processed_text + " Don't write anything other than command in output. The command is to be ran in CMD"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": context1}],
            model="llama-3.3-70b-versatile",
        )
        command = chat_completion.choices[0].message.content
        print(command)
        print(execute_command(command))

        explanation_text = processed_text + execute_command(command) + " Explain the output and what just happened in 50 words or less"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": explanation_text}],
            model="llama-3.3-70b-versatile",
        )
        explanation = chat_completion.choices[0].message.content
        print(explanation)

        audio = generate(
            text=explanation,
            voice="Lily",
            api_key="sk_8010becc719601aa3273d6d086b79952b666c57d52f898f5",
        )

        with open("output.wav", "wb") as f:
            f.write(audio)

        ding = 'ffmpeg -y -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)

        fpath = "foutput.wav"
        playwav(fpath)
    else:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": processed_text+" answer me COMPULSORILY in 10 words or less"}],
            model="llama-3.3-70b-versatile",
        )
        response = chat_completion.choices[0].message.content
        print(response)

        audio = generate(
            text=response,
            voice="Lily",
            api_key="sk_8010becc719601aa3273d6d086b79952b666c57d52f898f5",
        )

        with open("output.wav", "wb") as f:
            f.write(audio)

        ding = 'ffmpeg -y -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)

        fpath = "foutput.wav"
        playwav(fpath)

# GUI Setup with an Image and Text Bar
def start_gui():
    root = tk.Tk()
    root.title("Floating Mic")

    # Set a custom window icon (optional)
    icon_path = "icon.ico"  # Path to your icon file
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # Make the window draggable
    root.geometry("300x150")  # Initial size of the window
    root.attributes("-topmost", True)  # Keep window on top
    root.overrideredirect(False)  # Remove window borders and title bar

    # Function to make window draggable
    def on_drag(event):
        root.geometry(f'+{event.x_root}+{event.y_root}')

    # Add a frame for the content
    frame = tk.Frame(root)
    frame.pack()

    # Create a text bar for manual text input
    text_bar = tk.Entry(frame, font=("Arial", 12))
    text_bar.pack(pady=10)

    # Create a submit button for the text bar
    submit_button = tk.Button(
        frame,
        text="Submit",
        font=("Arial", 10),
        command=lambda: main_processing_function(text_bar.get())  # Pass input text
    )
    submit_button.pack(pady=5)

    # Create a close button
    close_button = tk.Button(
        frame,
        text="Close",
        font=("Arial", 10),
        command=root.destroy  # Close the GUI
    )
    close_button.pack(pady=5)
    import sys

    # Load the image and display it
    if getattr(sys, 'frozen', False):  # Check if running as a standalone executable
        img_path = os.path.join(sys._MEIPASS, "mic.png")  # Access bundled image
    else:
        img_path = os.path.join(os.path.dirname(__file__), "mic.png")  # Access local image

    img = Image.open(img_path)
    img = img.resize((30, 30), Image.Resampling.LANCZOS)  # Resize image to fit window
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(frame, image=photo)
    label.image = photo  # Keep a reference to prevent garbage collection
    label.pack()

    label.bind("<Button-1>", lambda event: main_processing_function())  # Run function on click

    # Make the window draggable
    frame.bind("<Button-1>", on_drag)

    root.mainloop()

# Start the GUI application
if __name__ == "__main__":
    start_gui()
