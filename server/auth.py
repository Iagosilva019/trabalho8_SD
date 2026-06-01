import hashlib
import secrets

tokens = {}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token(username, role):
    token = secrets.token_hex(32)

    tokens[token] = {
        "username": username,
        "role": role
    }

    return token


def validate_token(token):
    return tokens.get(token)
