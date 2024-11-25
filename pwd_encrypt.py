#/usr/bin/python3

# Type 7 Decryption and Encryption Example
TYPE7_KEY = "dsfd;kfoA,.iyewrkldJKDHSUB"

def decrypt(ciphertext):
    """Decrypt Cisco Type 7 password."""
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        enc_char = int(ciphertext[i:i+2], 16)
        key_char = ord(TYPE7_KEY[(i // 2) % len(TYPE7_KEY)])
        plaintext += chr(enc_char ^ key_char)
    return plaintext

def encrypt(plaintext):
    """Encrypt Cisco Type 7 password."""
    ciphertext = ""
    for i, char in enumerate(plaintext):
        enc_char = ord(char) ^ ord(TYPE7_KEY[i % len(TYPE7_KEY)])
        ciphertext += f"{enc_char:02x}"
    return ciphertext

# Example usage:
encrypted = encrypt("mypassword")
decrypted = decrypt(encrypted)

print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")