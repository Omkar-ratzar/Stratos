import os
from groq import Groq
client = Groq(
    api_key=("GROQ_API"),
)

def execute_command(command):
    result = os.popen(command).read()
    return result

#########################################################################speech to text
import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.AudioFile('nostratos.wav') as source:
    audio = recognizer.record(source)
try:
    text = recognizer.recognize_google(audio)
    print("Converted text:", text)
except sr.UnknownValueError:
    print("Speech not understood")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")

##############################################################################goes into if
if("stratos" in text):
    ##############################################################################runs the command
    context1= text+" Dont write anything other than command in output. The command is to be ran in CMD"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": context1,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    print(chat_completion.choices[0].message.content)
    print(execute_command(chat_completion.choices[0].message.content))

##############################################################################Explaining the command just ran
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text+execute_command(chat_completion.choices[0].message.content)+" Explain the output and what just happened in 50 words or less",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    print(chat_completion.choices[0].message.content)
    tempexplainaudio=chat_completion.choices[0].message.content

    import os
    from elevenlabs import voices, generate
    # Generate and play audio
    audio = generate(
        # text=chat_completion.choices[0].message.content,
        text=tempexplainaudio,
        voice="Lily",
        api_key="ELEVENLABSAPI"
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

#######################################################goes into else , nostratos
else:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    print(chat_completion.choices[0].message.content)

    import os
    from elevenlabs import voices, generate
    # Generate and play audio
    audio = generate(
        text=chat_completion.choices[0].message.content,
        voice="Lily",
        api_key="ELEVENLABSAPI"
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
