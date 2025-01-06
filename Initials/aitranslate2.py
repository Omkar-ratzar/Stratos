from transformers import AutoTokenizer, AutoModelForCausalLM

# Define model name
model_name = "meta-llama/LLaMA-3.2-3B"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name, token=True)
model = AutoModelForCausalLM.from_pretrained(model_name, token=True)


# Define a single prompt
prompt = "Hey there, where is mumbai located?"
 # Tokenize and generate
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_length=10+len(prompt),
    temperature=0.7,  # Keep it less random
    top_p=0.9,        # Reduce token options
    pad_token_id=tokenizer.eos_token_id,
    repetition_penalty=1.2  # Penalizes repeated text
)

# Decode and clean output
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
# Extract only the translation part

print(response)
