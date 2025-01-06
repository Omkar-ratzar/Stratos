#this translation is done using gptneo, check the model, its a open repo or something like that so be careful


from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "EleutherAI/gpt-neo-2.7B"  # Example open-access model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

prompt = "Hey there, where is Mumbai located??"

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_length=40,       # Limit output length to prevent excessive generation
    temperature=1.0,     # Controls randomness (lower values make output more deterministic)
    top_p=0.9,           # Nucleus sampling to keep high-probability tokens
    repetition_penalty=2.0  # Penalizes repeated text
)
print(tokenizer.decode(outputs[0]))


