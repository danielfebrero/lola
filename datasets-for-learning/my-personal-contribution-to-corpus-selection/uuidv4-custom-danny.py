import random

def generate_uuidv4_custom_danny(prefix="8f1639d7"):
    if len(prefix) != 8:
        raise ValueError("Prefix must be exactly 8 characters long")
    
    # Generate the remaining parts of the UUID
    time_low = prefix
    time_mid = ''.join(random.choices('0123456789abcdef', k=4))
    time_hi_and_version = f"4{random.choice('0123456789abcdef')}{random.choice('0123456789abcdef')}{random.choice('0123456789abcdef')}"
    clock_seq_hi_and_reserved = f"{random.choice('89ab')}{random.choice('0123456789abcdef')}"
    clock_seq_low = ''.join(random.choices('0123456789abcdef', k=2))
    node = ''.join(random.choices('0123456789abcdef', k=12))
    
    custom_uuid = f"{time_low}-{time_mid}-{time_hi_and_version}-{clock_seq_hi_and_reserved}{clock_seq_low}-{node}"
    return custom_uuid

# Print the generated UUIDV4-custom-danny
if __name__ == "__main__":
    uuid = generate_uuidv4_custom_danny()
    print(f"Conversation uuid: {uuid}")
