from crypt_utils import *
import os
from config import *

def encryptRoundRobin(i,data,key):
    mod4 = i%4
    if(mod4 == 0):
        return multiFernetEncrypt(data,key.keyMF1,key.keyMF2)
    elif(mod4==1):
        return ChaCha20Poly1305Encrypt(data,key.keyCH,key.aad,key.nonce)
    elif(mod4==2):
        return aesccmEncrypt(data,key.keyAESCCM,key.aad,key.nonce)
    elif(mod4==3):
        return aesgcmEncrypt(data,key.keyAESGCM,key.aad,key.nonce)

def decryptRoundRobin(i,data,key):
    mod4 = i%4
    if(mod4 == 0):
        return multiFernetDecrypt(data,key.keyMF1,key.keyMF2)
    elif(mod4==1):
        return ChaCha20Poly1305Decrypt(data,key.keyCH,key.aad,key.nonce)
    elif(mod4==2):
        return aesccmDecrypt(data,key.keyAESCCM,key.aad,key.nonce)
    elif(mod4==3):
        return aesgcmDecrypt(data,key.keyAESGCM,key.aad,key.nonce)

def getOutputFileName(path,blockNumber):
    return os.path.join(path,OUTPUT_FILE_SUCCESSOR_NAME+str(blockNumber)+OUTPUT_FILE_EXTENSION)

def splitAndEncrypt(file,folder,key):
    if not os.path.exists(folder):
        os.makedirs(folder)

    targetPath = os.path.join(folder,file)
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)

    with open(file,'rb') as f:
        data = f.read(BLOCK_SIZE)
        block=0
        while(data):
            outputFileName = getOutputFileName(targetPath,block)
            with open(outputFileName,'wb') as outfile:
                outfile.write(encryptRoundRobin(block,data,key))
            block+=1
            data = f.read(BLOCK_SIZE)

def sort_enc_filenames(filenames):
    sorted_filenames = sorted(filenames, key=lambda x: int(x.split('.')[0][3:]))
    return sorted_filenames

def splitAndDecrypt(file,folder,key,targetDirectory):
    path = os.path.join(folder,file)
    outfileName = os.path.join(targetDirectory,file)
    if not os.path.exists(path):
        raise Exception("Invalid path")
    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
    files =sort_enc_filenames(os.listdir(path))
    with open(outfileName,'wb') as outfile:
        block=0
        for infile in files:
            with open(os.path.join(folder,file,infile),'rb') as infilePointer:
                outfile.write(decryptRoundRobin(block,infilePointer.read(),key))
            block+=1

def deleteFile(file):
    os.unlink(file)



    



