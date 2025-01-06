from gtts import gTTS
#pip install gtts
language = 'en'
text="Hello world, This is my second test in turning text to speech"
speech = gTTS(text=text,lang=language,slow=False,tld="co.in")
speech.save("T2S.mp3")
