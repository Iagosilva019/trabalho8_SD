from cryptography.fernet import Fernet
import os

KEY_FILE = "key.key"

if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as f:
        f.write(Fernet.generate_key())

with open(KEY_FILE, "rb") as f:
    KEY = f.read()

fernet = Fernet(KEY)


def encrypt_message(message):
    return fernet.encrypt(message.encode())


def decrypt_message(cipher_text):
    return fernet.decrypt(cipher_text).decode()
