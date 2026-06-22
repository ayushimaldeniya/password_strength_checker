import os
import hashlib
import secrets

def generate_secure_salt(byte_length: int = 16) -> str:
    """Generates a cryptographically secure random salt using the operating system's
    highest quality entropy source (secret module)."""
    return secrets.token_hex(byte_length)  #secrets.token_hex(16) creates a 32-character hexadecimal string

def compute_salted_hash(password: str, salt: str) -> str:
    """Combines a plaintext passwords with a unique salt string and computes a
    one-way cryptographic hash using SHA-256."""
    #1. Combine the password and salt
    salted_password = password + salt

    #2. Encode the string into raw binary bytes
    payload_bytes = salted_password.encode('utf-8')

    #3. Derive the one way cryptographic signature block
    hash_object = hashlib.sha256(payload_bytes)

    #4. Extract the clean hexadecimal string representation of the hash
    return hash_object.hexdigest()

def verify_password_signature(input_password: str, stored_hash: str, stored_salt: str) -> bool:
    """Validates a login attemot by re-hashing the input password with the stored salt
    and verifying if it mathematically mirrors the original database record."""
    #1. Recompute the hash using the input password and the stored salt
    new_hash = compute_salted_hash(input_password, stored_salt)

    #2. Use hmac.compare_digest or constant-time check to prevent timing analysis attacks
    return secrets.compare_digest(new_hash, stored_hash)