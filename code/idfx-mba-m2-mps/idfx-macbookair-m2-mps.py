import os
import torch
from transformers import AutoTokenizer, AutoConfig, IdeficsForVisionText2Text, IdeficsConfig
from safetensors.torch import load_file
from PIL import Image
import psutil
import time

def print_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"RSS: {memory_info.rss / (1024 ** 2):.2f} MB")
    print(f"VMS: {memory_info.vms / (1024 ** 2):.2f} MB")

# Check if MPS is available and set the device accordingly
if torch.backends.mps.is_available():
    DEVICE = torch.device('mps')
    print("Using MPS device")
else:
    DEVICE = torch.device('cpu')
    print("MPS device not available, using CPU")

print_memory_usage()

# Define the model directory
model_dir = "./code/idfx-mba-m2-mps/idefics"  # Update the path as needed

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_dir)
print_memory_usage()

# Load the model configuration
config = IdeficsConfig.from_pretrained(model_dir)
print_memory_usage()

# Load the model weights from safetensors
model = IdeficsForVisionText2Text(config)
model_weights_path = os.path.join(model_dir, "adapter_model.safetensors")
state_dict = load_file(model_weights_path)
model.load_state_dict(state_dict, strict=False)  # Allow some flexibility in loading
print_memory_usage()

# Quantize the model dynamically
model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
print_memory_usage()

# Move the model to the appropriate device (CPU or MPS)
model.to(DEVICE)
print_memory_usage()

# Define the input data
data = {"inputs": ["Hello, how are you?", "What's the weather today?"]}

# Extract inputs from data
inputs_text = data.get("inputs")

# Tokenize the input text in smaller chunks
inputs = tokenizer(inputs_text, padding=True, truncation=True, return_tensors="pt").to(DEVICE)
print_memory_usage()

# Load and preprocess an image (example image path provided)
image_path = "path/to/your/image.jpg"  # Replace with your image path
image = Image.open(image_path)
image = image.resize((224, 224))  # Resize to expected input size
pixel_values = torch.tensor(image).unsqueeze(0).to(DEVICE)  # Convert to tensor and move to device

# Generate text using the model
with torch.no_grad():  # Disable gradient calculation
    generated_ids = model.generate(pixel_values=pixel_values, **inputs, max_new_tokens=50)  # Provide pixel_values
    generated_texts = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

print(generated_texts)
print_memory_usage()
