from utils import *
from config import AAD,KEY_EXTENSION

class Key():
    def generateKeys(self):
        self.keyMF1 = generateFernetKey()
        self.keyMF2 = generateFernetKey()
        self.keyCH = generateChaCha20Poly1305Key()
        self.keyAESCCM = generateAESCCMKey()
        self.keyAESGCM = generateAESGCMKey()
        self.nonce = generateNonce(12)
        self.aad = AAD

    def writeToDisk(self,file,folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        if(not file.endswith(KEY_EXTENSION)):
            raise Exception("PEM file needed")
        with open(os.path.join(folder,file), 'wb') as keyFile:
            keyFile.writelines([b'::::KEY START--------------\n::::',self.keyMF1+'\n::::'.encode(),self.keyMF2+'\n::::'.encode(),self.keyCH+'\n::::'.encode(),self.keyAESCCM+'\n::::'.encode(),self.keyAESGCM+'\n::::'.encode(),self.nonce+'\n::::'.encode(),self.aad.encode()+'\n::::'.encode(),b'KEY END--------------'])
        
    def readFromDisk(self,file,folder):
        targetFile = os.path.join(folder,file)
        if not os.path.exists(targetFile):
            raise Exception("Key file does not exist")
        with open(targetFile, 'rb') as keyFile:
            keyList =keyFile.read().split("::::".encode())
            self.keyMF1 = keyList[2][:-1]
            self.keyMF2 = keyList[3][:-1]
            self.keyCH = keyList[4][:-1]
            self.keyAESCCM = keyList[5][:-1]
            self.keyAESGCM = keyList[6][:-1]
            self.nonce = keyList[7][:-1]
            self.aad = keyList[8][:-1].decode()
    
    def getKeyAsByteString(self):
        return b'::::KEY START--------------\n::::'+self.keyMF1+'\n::::'.encode()+self.keyMF2+'\n::::'.encode()+self.keyCH+'\n::::'.encode()+self.keyAESCCM+'\n::::'.encode()+self.keyAESGCM+'\n::::'.encode()+self.nonce+'\n::::'.encode()+self.aad.encode()+'\n::::'.encode()+b'KEY END--------------'
        
        
