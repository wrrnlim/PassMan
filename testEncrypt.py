from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# encrypt
masterPass = 'password'
password = masterPass.encode() # convert to bytes

salt = b'w\tN\xd8\xf1[k\x97\xc3=\xc9\x90k\xde\xe8\xad'

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256,
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)

key = base64.urlsafe_b64encode(kdf.derive(password))
print('Key:',key)

message = 'hello world'
f = Fernet(key)
encryptedMsg = f.encrypt(message.encode())
print('Encrypted message:',encryptedMsg)

# decrypt
f2 = Fernet(key)
decryptedMsg = f2.decrypt(encryptedMsg)
msg = decryptedMsg.decode()
print('The message was:',msg)