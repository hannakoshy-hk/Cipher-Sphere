from cryptography.fernet import Fernet,MultiFernet
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def generateFernetKey():
    return Fernet.generate_key()

def generateChaCha20Poly1305Key():
    return ChaCha20Poly1305.generate_key()

def generateAESGCMKey():
    return AESGCM.generate_key(bit_length=128)

def generateAESCCMKey():
    return AESCCM.generate_key(bit_length=128)

def fernetEncrypt(data,key):
    f = Fernet(key)
    return f.encrypt(data)

def fernetDecrypt(data,key):
    f = Fernet(key)
    return f.decrypt(key)

def ChaCha20Poly1305Encrypt(data,key,aad,nonce):
    f = ChaCha20Poly1305(key)
    return f.encrypt(nonce,data,aad.encode())

def ChaCha20Poly1305Decrypt(data,key,aad,nonce):
    f = ChaCha20Poly1305(key)
    return f.decrypt(nonce,data,aad.encode())

def multiFernetEncrypt(data,key1,key2):
    f = MultiFernet([Fernet(key1),Fernet(key2)])
    return f.encrypt(data)

def multiFernetDecrypt(data,key1,key2):
    f = MultiFernet([Fernet(key1),Fernet(key2)])
    return f.decrypt(data)

def aesccmEncrypt(data,key,aad,nonce):
    f = AESCCM(key)
    return f.encrypt(nonce,data,aad.encode())

def aesccmDecrypt(data,key,aad,nonce):
    f = AESCCM(key)
    return f.decrypt(nonce,data,aad.encode())

def aesgcmEncrypt(data,key,aad,nonce):
    f = AESGCM(key)
    return f.encrypt(nonce,data,aad.encode())

def aesgcmDecrypt(data,key,aad,nonce):
    f = AESGCM(key)
    return f.decrypt(nonce,data,aad.encode())

def generateNonce(length):
    return os.urandom(length)
