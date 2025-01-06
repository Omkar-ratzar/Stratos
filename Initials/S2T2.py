import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.AudioFile('stratos1.wav') as source:
    audio = recognizer.record(source)
try:
    text = recognizer.recognize_google(audio)
    print("Converted text:", text)
except sr.UnknownValueError:
    print("Speech not understood")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
