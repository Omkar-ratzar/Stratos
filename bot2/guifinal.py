import tkinter as tk
import threading
from guitest1 import execute_command


def start_listening():
    def process_audio():
        try:
            print("Listening for Audio input")
            main_p
        except Exception as e:
            print(f"Error during processing: {e}")
    threading.Thread(target=process_audio,daemon=True).start()

root=tk.Tk()
root.title("Floating Mic")
root.geometry("100x100")
root.resizable(False,False)
root.attributes("-topmost",True)
root.overrideredirect(True)

button = tk.Button(root, text="🎤", bg="red", fg="white", font=("Arial", 24), command=start_listening)
button.pack(expand=True, fill=tk.BOTH)

# Make the window draggable
def start_drag(event):
    root.x = event.x
    root.y = event.y

def stop_drag(event):
    root.geometry(f"+{event.x_root-root.x}+{event.y_root-root.y}")

button.bind("<Button-1>", start_drag)
button.bind("<B1-Motion>", stop_drag)

# Run the GUI loop
root.mainloop()


##now finally defining the main_p
import os
from groq import Groq
import speech_recognition as sr
import os
from elevenlabs import voices, generate


def main_p():
    # Step 1: Speech to Text
    recognizer = sr.Recognizer()
    with sr.AudioFile('nostratos.wav') as source:
        audio = recognizer.record(source)

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
            api_key="sk_0d86ca6a5ca581587348fbedff77531fa3c4544fe4d1e547"
        )

        with open("output.wav", "wb") as f:
            f.write(audio)

        # Convert to proper format for playback
        ding = 'ffmpeg -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)

        from playsound import playsound
        playsound("foutput.wav")

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
            api_key="sk_0d86ca6a5ca581587348fbedff77531fa3c4544fe4d1e547"
        )

        with open("output.wav", "wb") as f:
            f.write(audio)

        # Convert to proper format for playback
        ding = 'ffmpeg -i "output.wav" -acodec pcm_s16le -ar 44100 -ac 2 foutput.wav'
        execute_command(ding)

        from playsound import playsound
        playsound("foutput.wav")
