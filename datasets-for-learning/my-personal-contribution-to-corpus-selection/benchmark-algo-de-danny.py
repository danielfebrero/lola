import os
import math
from collections import Counter
from timeit import timeit
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Define S-box and P-box
S_BOX = [
    0x6, 0x4, 0xC, 0x5, 0x0, 0x7, 0x2, 0xE,
    0x1, 0xF, 0x3, 0xD, 0x8, 0xA, 0x9, 0xB
]

P_BOX = [
    0, 4, 8, 12, 1, 5, 9, 13,
    2, 6, 10, 14, 3, 7, 11, 15
]

def s_box_substitution(n):
    return S_BOX[n]

def p_box_permutation(bits):
    permuted_bits = 0
    for i in range(16):
        bit = (bits >> i) & 1
        permuted_bits |= (bit << P_BOX[i])
    return permuted_bits

def generate_round_keys(key, rounds):
    round_keys = []
    for i in range(rounds):
        round_key = (key >> (i * 4)) & 0xFFFF
        round_keys.append(round_key)
    return round_keys

def encrypt_spn(plaintext, key, rounds=4):
    state = plaintext
    round_keys = generate_round_keys(key, rounds)
    
    for i in range(rounds - 1):
        # Apply S-box substitution
        state = (s_box_substitution((state >> 12) & 0xF) << 12) | \
                (s_box_substitution((state >> 8) & 0xF) << 8) | \
                (s_box_substitution((state >> 4) & 0xF) << 4) | \
                s_box_substitution(state & 0xF)
        
        # Apply P-box permutation
        state = p_box_permutation(state)
        
        # XOR with round key
        state ^= round_keys[i]
    
    # Last round: only apply S-box substitution and final XOR with round key
    state = (s_box_substitution((state >> 12) & 0xF) << 12) | \
            (s_box_substitution((state >> 8) & 0xF) << 8) | \
            (s_box_substitution((state >> 4) & 0xF) << 4) | \
            s_box_substitution(state & 0xF)
    
    state ^= round_keys[-1]
    
    return state

def decrypt_spn(ciphertext, key, rounds=4):
    state = ciphertext
    round_keys = generate_round_keys(key, rounds)
    
    # First round: only apply XOR with round key and inverse S-box substitution
    state ^= round_keys[-1]
    state = (S_BOX.index((state >> 12) & 0xF) << 12) | \
            (S_BOX.index((state >> 8) & 0xF) << 8) | \
            (S_BOX.index((state >> 4) & 0xF) << 4) | \
            S_BOX.index(state & 0xF)
    
    for i in range(rounds - 2, -1, -1):
        # XOR with round key
        state ^= round_keys[i]
        
        # Apply inverse P-box permutation
        state = p_box_permutation(state)
        
        # Apply inverse S-box substitution
        state = (S_BOX.index((state >> 12) & 0xF) << 12) | \
                (S_BOX.index((state >> 8) & 0xF) << 8) | \
                (S_BOX.index((state >> 4) & 0xF) << 4) | \
                S_BOX.index(state & 0xF)
    
    return state

# Utility functions to convert between strings and integers
def string_to_int(s):
    return int.from_bytes(s.encode(), 'big')

def int_to_string(i, length):
    return i.to_bytes(length, 'big').decode()

# Shannon entropy calculation
def shannon_entropy(data):
    if not data:
        return 0
    entropy = 0
    length = len(data)
    counts = Counter(data)
    for count in counts.values():
        p_x = count / length
        entropy += - p_x * math.log2(p_x)
    return entropy

# AES encryption and decryption
def encrypt_aes(plaintext, key, iv):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext.encode()) + encryptor.finalize()

def decrypt_aes(ciphertext, key, iv):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# DES encryption and decryption
def encrypt_des(plaintext, key, iv):
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext.encode()) + encryptor.finalize()

def decrypt_des(ciphertext, key, iv):
    backend = default_backend()
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Benchmarking
def benchmark():
    key = 0x3A94D63F
    plaintext = "Hello, World!" * 100  # Larger text for better benchmarking
    plaintext_int = string_to_int(plaintext)
    
    # AES and DES require key and IV
    key_aes = os.urandom(32)
    iv_aes = os.urandom(16)
    key_des = os.urandom(24)
    iv_des = os.urandom(8)

    # Ensure plaintext length is a multiple of block size for AES and DES
    padded_plaintext = plaintext + " " * ((16 - len(plaintext) % 16) % 16)
    
    # SPN encryption benchmark
    spn_encrypt_time = timeit(lambda: encrypt_spn(plaintext_int, key), number=100)
    ciphertext_spn = encrypt_spn(plaintext_int, key)
    spn_decrypt_time = timeit(lambda: decrypt_spn(ciphertext_spn, key), number=100)
    ciphertext_bytes_spn = ciphertext_spn.to_bytes((ciphertext_spn.bit_length() + 7) // 8, byteorder='big')
    entropy_spn = shannon_entropy(ciphertext_bytes_spn)
    
    print(f"SPN Encrypt Time: {spn_encrypt_time} seconds")
    print(f"SPN Decrypt Time: {spn_decrypt_time} seconds")
    print(f"SPN Algorithm Entropy: {entropy_spn}")

    # AES encryption benchmark
    aes_encrypt_time = timeit(lambda: encrypt_aes(padded_plaintext, key_aes, iv_aes), number=100)
    ciphertext_aes = encrypt_aes(padded_plaintext, key_aes, iv_aes)
    aes_decrypt_time = timeit(lambda: decrypt_aes(ciphertext_aes, key_aes, iv_aes), number=100)
    entropy_aes = shannon_entropy(ciphertext_aes)
    
    print(f"AES Encrypt Time: {aes_encrypt_time} seconds")
    print(f"AES Decrypt Time: {aes_decrypt_time} seconds")
    print(f"AES Algorithm Entropy: {entropy_aes}")

    # DES encryption benchmark
    des_encrypt_time = timeit(lambda: encrypt_des(padded_plaintext, key_des, iv_des), number=100)
    ciphertext_des = encrypt_des(padded_plaintext, key_des, iv_des)
    des_decrypt_time = timeit(lambda: decrypt_des(ciphertext_des, key_des, iv_des), number=100)
    entropy_des = shannon_entropy(ciphertext_des)
    
    print(f"DES Encrypt Time: {des_encrypt_time} seconds")
    print(f"DES Decrypt Time: {des_decrypt_time} seconds")
    print(f"DES Algorithm Entropy: {entropy_des}")

if __name__ == "__main__":
    benchmark()
