#!/usr/bin/env python3

import argparse
import os
import binascii
import pyspx
import pyspx.shake_128f as sphincs

def keygen():
    """Generate a SPHINCS+ keypair and save to files."""
    try:
        # Generate a random seed 
        seed = os.urandom(sphincs.crypto_sign_SEEDBYTES)

        # Generate a new keypair
        public_key, private_key = sphincs.generate_keypair(seed)

        # Convert keys to hex for storage
        public_key_hex = binascii.hexlify(public_key).decode('ascii')
        private_key_hex = binascii.hexlify(private_key).decode('ascii')

        # Save public key to file
        try:
            with open('public_key.hex', 'w') as f:
                f.write(public_key_hex)
        except IOError as e:
            print(f"Error writing public key file: {e}")
            return

        # Save private key to file
        try:
            with open('private_key.hex', 'w') as f:
                f.write(private_key_hex)
        except IOError as e:
            print(f"Error writing private key file: {e}")
            return

        # Print the keypair generation information
        print("Keypair generated:")
        print(f"- Public key: {public_key_hex}")
        print(f"- Private key: {private_key_hex}")

    except Exception as e:
        print(f"Error generating keypair: {e}")

def sign(file_path):
    """Sign a file using SPHINCS+ and save the signature to a file."""
    try:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return

        # Load the private key
        if not os.path.exists('private_key.hex'):
            print("Error: Private key not found. Run --keygen first.")
            return

        try:
            with open('private_key.hex', 'r') as f:
                private_key_hex = f.read().strip()  # .strip() removes trailing newlines or whitespace
        except IOError as e:
            print(f"Error reading private key file: {e}")
            return

        private_key = binascii.unhexlify(private_key_hex)

        # Read the file content
        with open(file_path, 'rb') as f:
            message = f.read()

        # Sign the message
        signature = sphincs.sign(message, private_key)

        # Convert signature to hex and save to file
        signature_hex = binascii.hexlify(signature).decode('ascii')
        try:
            with open('signature.hex', 'w') as f:
                f.write(signature_hex)
        except IOError as e:
            print(f"Error writing signature file: {e}")
            return

        # Print the signature generation information
        print("Signature generated:")
        print(f"- Signature: {signature_hex}")
    except Exception as e:
        print(f"Error signing file: {e}")

def verify(file_path, signature_path, public_key_path):
    """Verify a file's signature using SPHINCS+."""
    try:
        # Check if all files exist
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return
        if not os.path.exists(signature_path):
            print(f"Error: Signature file '{signature_path}' not found.")
            return
        if not os.path.exists(public_key_path):
            print(f"Error: Public key file '{public_key_path}' not found.")
            return

        # Load the public key
        try:
            with open(public_key_path, 'r') as f:
                public_key_hex = f.read().strip()
        except IOError as e:
            print(f"Error reading public key file: {e}")
            return

        # Load the signature
        try:
            with open(signature_path, 'r') as f:
                signature_hex = f.read().strip()
        except IOError as e:
            print(f"Error reading signature file: {e}")
            return

        # Read the file content
        try:
            with open(file_path, 'rb') as f:
                message = f.read()
        except IOError as e:
            print(f"Error reading file to verify: {e}")
            return

        # Convert hex to bytes
        try:
            public_key = binascii.unhexlify(public_key_hex)
            signature = binascii.unhexlify(signature_hex)
        except binascii.Error as e:
            print(f"Error decoding hex data: {e}")
            return

        # Verify the signature
        try:
            result = sphincs.verify(message, signature, public_key)
            print(f"Signature Verification result: {result}")
        except Exception as e:
            print("Signature Verification result: False")
            print(f"Error during verification: {str(e)}")
    except Exception as e:
        print(f"Error verifying signature: {e}")

def main():
    try:
        parser = argparse.ArgumentParser(description='SPHINCS+ Digital Signature Tool')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--keygen', action='store_true', help='Generate a new keypair')
        group.add_argument('--sign', metavar='FILE', help='Sign the specified file')
        group.add_argument('--verify', metavar='FILE', help='Verify a signature for the specified file')

        parser.add_argument('signature', nargs='?', help='Path to the signature file (for --verify)')
        parser.add_argument('public_key', nargs='?', help='Path to the public key file (for --verify)')

        args = parser.parse_args()

        if args.keygen:
            keygen()
        elif args.sign:
            sign(args.sign)
        elif args.verify:
            if not args.signature or not args.public_key:
                parser.error("--verify requires signature and public_key paths")
            verify(args.verify, args.signature, args.public_key)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
