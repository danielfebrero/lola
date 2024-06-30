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

# Generate 10 custom UUIDs
def generate_custom_uuids(n=1):
    custom_uuids = [generate_uuidv4_custom_danny() for _ in range(n)]
    return custom_uuids

# Print the generated UUIDs
if __name__ == "__main__":
    uuids = generate_custom_uuids(1)
    for i, uuid in enumerate(uuids):
        print(f"Conversation uuid: {uuid}")
