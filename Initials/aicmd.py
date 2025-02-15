

from transformers import AutoTokenizer, AutoModelForCausalLM

# Define model name
model_name = "meta-llama/LLaMA-3.2-3B"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name, token=True)
model = AutoModelForCausalLM.from_pretrained(model_name, token=True)
# Define the prompt
prompt = (
    "Write a PowerShell script that monitors CPU usage using the `Get-Counter` cmdlet "
    "every 5 seconds and appends the output to a file named `cpu_log.txt`."
)

# Generate the output
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_length=150,
    temperature=0.5,
    top_p=0.9,
    pad_token_id=tokenizer.eos_token_id,
)

# Decode and print the result
powershell_script = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(powershell_script)
