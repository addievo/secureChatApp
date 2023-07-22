from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding


def generate_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

#changing message to bytes using utf-8 encoding
def encrypt_message(public_key, message):
    message_bytes = message.encode('utf-8')
    encrypted_message = public_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

#decrypting from bytes to string using utf-8 encoding
def decrypt_message(private_key, encrypted_message):
    decrypted_message_bytes = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    decrypted_message = decrypted_message_bytes.decode('utf-8')
    return decrypted_message
