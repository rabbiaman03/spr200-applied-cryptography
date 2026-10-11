import getpass
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

student_id = "demo"  # label used in key file names

# Load private key (passphrase entered at runtime)
with open(f'private_key_RSA_encrypted_{student_id}.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=getpass.getpass('Passphrase for private key: ').encode(),
        backend=default_backend()
    )

# Load public key
with open(f'public_key_RSA_{student_id}.pem', 'rb') as f:
    public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )

# Encrypt file
with open('encrypt_it.txt', 'rb') as f:
    plaintext = f.read()

ciphertext = public_key.encrypt(
    plaintext,
    padding.PKCS1v15()
)

with open('file_encrypted.bin', 'wb') as f:
    f.write(ciphertext)

# Decrypt file
with open('file_encrypted.bin', 'rb') as f:
    ciphertext = f.read()

plaintext = private_key.decrypt(
    ciphertext,
    padding.PKCS1v15()
)

with open('file_decrypted.txt', 'wb') as f:
    f.write(plaintext)

print("Encryption/Decryption completed!")