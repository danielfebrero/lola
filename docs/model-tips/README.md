# Correctly exploit your model (benchmark results issued by simulation)

- reduce memory consumption by 30%
- increase inference spead by 30%
- accuracy will vary from -1% (because of float16) to +x% (because of 9B)

https://chatgpt.com/share/b4f81846-d103-4921-8905-aeab2b540cb3

## GPU

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
processor = AutoProcessor.from_pretrained("enghamdiali/idefics-9b-qt_f")
model = AutoModelForVision2Seq.from_pretrained(
    "HuggingFaceM4/idefics2-8b",
    torch_dtype=torch.float16
).to(DEVICE)
```

## CPU

See ../code/idefics-cpu.py
