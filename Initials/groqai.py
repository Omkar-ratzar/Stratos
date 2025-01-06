import os

from groq import Groq

client = Groq(
    api_key=("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"),
)
def execute_command(command):
    result = os.popen(command).read()
    return result
inz=str(input())
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": inz,
        }
    ],
    model="llama-3.3-70b-versatile",
)

def sound(text):
    import os
    from elevenlabs import voices, generate
    # Generate and play audio
    audio = generate(
        text=text,
        voice="Lily",
        api_key="sk_0d86ca6a5ca581587348fbedff77531fa3c4544fe4d1e547"
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

print(chat_completion.choices[0].message.content)
#print(execute_command(chat_completion.choices[0].message.content))
sound(chat_completion.choices[0].message.content)
