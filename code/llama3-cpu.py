import torch
from typing import Dict, List, Any
from transformers import AutoProcessor, AutoModelForCausalLM

# Set the device to CPU
DEVICE = torch.device('cpu')
processor = AutoProcessor.from_pretrained("TheSkullery/llama-3-cat-8b-instruct-v1")
model = AutoModelForCausalLM.from_pretrained(
            "TheSkullery/llama-3-cat-8b-instruct-v1",
            torch_dtype=torch.float32  # Use float32 for CPU
        ).to(DEVICE)
model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.qint8
        )

data = {"inputs": ["Hello, how are you?", "What's the weather today?"]}

 # Extract inputs from data
inputs_text = data.get("inputs")

# Process the inputs
inputs = processor(text=inputs_text, padding=True, return_tensors="pt")
inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

# Generate text using the model
generated_ids = model.generate(**inputs, max_new_tokens=500)
generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)

print(generated_texts)
