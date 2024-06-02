# Unleash model performances

- reduce memory consumption by 50%
- increase inference spead by x3
- response accuracy drop from 95% to 94% (if you can live with it)

## How to do it (GPU)

Replace

```python
DEVICE = "cuda:0"
processor = AutoProcessor.from_pretrained("HuggingFaceM4/idefics2-8b")
model = AutoModelForVision2Seq.from_pretrained(
    "HuggingFaceM4/idefics2-8b",
).to(DEVICE)
```

with

```python
DEVICE = torch.cuda('cuda:0')
processor = AutoProcessor.from_pretrained("HuggingFaceM4/idefics2-8b")
model = AutoModelForVision2Seq.from_pretrained(
    "HuggingFaceM4/idefics2-8b",
    torch_dtype=torch.float16
).to(DEVICE)
```

## CPU

```python
import torch
from typing import Dict, List, Any
from transformers import AutoProcessor, AutoModelForSeq2SeqLM

# Set the device to CPU
DEVICE = torch.device('cpu')

class EndpointHandler:
    def __init__(self, path=""):
        # Load processor and model
        self.processor = AutoProcessor.from_pretrained("Llama3Model/llama3-base")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "Llama3Model/llama3",
            torch_dtype=torch.float32  # Use float32 for CPU
        ).to(DEVICE)

        # Apply dynamic quantization for inference speed-up on CPU
        self.model = torch.quantization.quantize_dynamic(
            self.model, {torch.nn.Linear}, dtype=torch.qint8
        )

    def __call__(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Args:
            data (Dict[str, Any]): Data dictionary containing 'inputs'
        Returns:
            List[Dict[str, Any]]: Generated texts
        """
        # Extract inputs from data
        inputs_text = data.get("inputs")

        # Process the inputs
        inputs = self.processor(text=inputs_text, padding=True, return_tensors="pt")
        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

        # Generate text using the model
        generated_ids = self.model.generate(**inputs, max_new_tokens=500)
        generated_texts = self.processor.batch_decode(generated_ids, skip_special_tokens=True)

        return generated_texts

# Example usage
# handler = EndpointHandler()
# result = handler({"inputs": ["Hello, how are you?", "What's the weather today?"]})
# print(result)
```
