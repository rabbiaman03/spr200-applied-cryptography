# Lab 5 — RSA Encryption and Ed25519 Signatures in Python

**Author:** Rabbi Muhammad Aman · **Course:** SPR200 (Winter 2025)

| Script | What it does |
|---|---|
| [`gen_rsa_keys.py`](gen_rsa_keys.py) | Generates an RSA-2048 key pair (e = 65537). Saves the private key as PKCS#8, **encrypted with a passphrase** |
| [`rsa_encrypt_decrypt.py`](rsa_encrypt_decrypt.py) | Encrypts `encrypt_it.txt` with the public key and decrypts it with the private key (PKCS#1 v1.5 padding) |
| [`ed25519_sign.py`](ed25519_sign.py) | Generates an Ed25519 key pair and signs `encrypt_it.txt` |
| [`ed25519_verify.py`](ed25519_verify.py) | Verifies the Ed25519 signature |

## Run
```bash
pip install cryptography
echo "hello crypto" > encrypt_it.txt
python gen_rsa_keys.py            # prompts for a passphrase
python rsa_encrypt_decrypt.py     # prompts for the same passphrase
python ed25519_sign.py && python ed25519_verify.py
```

## Notes
- Keys are generated locally and are **never committed** (`*.pem` is git-ignored).
- PKCS#1 v1.5 is used here because the lab required it. New designs should use **RSA-OAEP** for encryption.
- Ed25519 gives small, fast, deterministic signatures, and avoids the nonce-reuse pitfalls of ECDSA.
