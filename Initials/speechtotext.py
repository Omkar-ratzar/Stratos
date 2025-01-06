from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
atest=pipeline("automatic-speech-recognition")

res=atest("natural.wav")

print(res)
