"""Implementation of the functions to encrypt and decrypt a password."""
from cryptography.fernet import Fernet

def encrypt_message(message):
    """
    Function to encrypt the password.
    """
    key = open("secret.key", "rb").read()
    encoded_message = message.encode()
    f = Fernet(key.decode())

    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message


def decrypt_message(encrypted_message):
    """
        Function to decrypt the password.
    """
    key = open("secret.key", "rb").read()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message.decode()
