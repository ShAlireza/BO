import secrets
import string


def generate_secret_key(length=64):
    chars = string.ascii_letters + string.digits + "@$#!.<=>+-_?*%"
    key = ''.join(secrets.choice(chars) for _ in range(length))

    return key


def generate_token_key(length=64):
    return secrets.token_hex(length)
