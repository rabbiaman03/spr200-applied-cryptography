from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

student_id = "demo"  # label used in key file names

# Load public key
with open(f"public_key_Ed25519_{student_id}.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Load signature
with open(f"signature_Ed25519_{student_id}.bin", "rb") as f:
    signature = f.read()

# Verify signature
try:
    with open("encrypt_it.txt", "rb") as f:
        data = f.read()
    public_key.verify(signature, data)
    print("Signature verification successful.")
except InvalidSignature:
    print("Signature verification failed.")