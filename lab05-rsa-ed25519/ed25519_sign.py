from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

student_id = "demo"  # label used in key file names

# Generate Ed25519 key pair
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Save private key
with open(f"private_key_Ed25519_{student_id}.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Save public key
with open(f"public_key_Ed25519_{student_id}.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

# Sign file
with open("encrypt_it.txt", "rb") as f:
    data = f.read()

signature = private_key.sign(data)

# Save signature
with open(f"signature_Ed25519_{student_id}.bin", "wb") as f:
    f.write(signature)

print("File signed successfully.")
