import os
import torch
from transformers import AutoTokenizer
from transformers.models.idefics import IdeficsForVisionText2Text, IdeficsConfig
from safetensors.torch import load_file

# Check if MPS is available and set device accordingly
DEVICE = torch.device('mps') if torch.backends.mps.is_available() else torch.device('cpu')

# Define the model directory
model_dir = "./code/idfx-mba-m2-mps/idefics"  # Update the path as needed

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_dir)

# Load the model configuration
config = IdeficsConfig.from_pretrained(model_dir)

# Load the model weights from safetensors
model = IdeficsForVisionText2Text(config)
model_weights_path = os.path.join(model_dir, "adapter_model.safetensors")
state_dict = load_file(model_weights_path)
model.load_state_dict(state_dict, strict=False)  # Allow some flexibility in loading

# Move the model to the appropriate device (MPS or CPU)
model.to(DEVICE)

# Quantize the model dynamically if running on CPU (quantization isn't supported on MPS)
if DEVICE == torch.device('cpu'):
    model = torch.quantization.quantize_dynamic(
        model, {torch.nn.Linear}, dtype=torch.qint8
    )

# Define the input data
data = {"inputs": ["Hello, how are you?", "What's the weather today?"]}

# Extract inputs from data
inputs_text = data.get("inputs")

# Example of reducing batch size
inputs = tokenizer.batch_encode_plus(inputs_text, padding=True, truncation=True, return_tensors="pt", max_length=128).to(DEVICE)

# Generate text using the model
with torch.no_grad():  # Disable gradient calculation
    generated_ids = model.generate(**inputs, max_new_tokens=50)  # Reduce max_new_tokens to lower memory usage
    generated_texts = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

print(generated_texts)
