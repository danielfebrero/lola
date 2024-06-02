import os
import torch
from transformers import AutoTokenizer, AutoConfig
from transformers.models.idefics import IdeficsForVisionText2Text, IdeficsConfig
from safetensors.torch import load_file

# Check if MPS is available and set the device accordingly
if torch.backends.mps.is_available():
    DEVICE = torch.device('mps')
    print("Using MPS device")
else:
    DEVICE = torch.device('cpu')
    print("MPS device not available, using CPU")

# Define the model directory
model_dir = "../idfx"  # Update the path as needed

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_dir)

# Load the model configuration
config = IdeficsConfig.from_pretrained(model_dir)

# Load the model weights from safetensors
model = IdeficsForVisionText2Text(config)
model_weights_path = os.path.join(model_dir, "adapter_model.safetensors")
state_dict = load_file(model_weights_path)
model.load_state_dict(state_dict, strict=False)  # Allow some flexibility in loading

# Quantize the model dynamically
model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# Move the model to the appropriate device (CPU or MPS)
model.to(DEVICE)

# Define the input data
data = {"inputs": ["Hello, how are you?", "What's the weather today?"]}

# Extract inputs from data
inputs_text = data.get("inputs")

# Tokenize the input text in smaller chunks
inputs = tokenizer(inputs_text, padding=True, truncation=True, return_tensors="pt").to(DEVICE)

# Generate text using the model
with torch.no_grad():  # Disable gradient calculation
    generated_ids = model.generate(**inputs, max_new_tokens=50)  # Reduce max_new_tokens to lower memory usage
    generated_texts = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

print(generated_texts)
