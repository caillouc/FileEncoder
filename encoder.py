from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import time
import getpass
import json
import base64
import sys

#saltFileName = ".encoderFileSalt"
saltFileName = "/Volumes/SALT/.encoderFileSalt"


def loadSalt():
    """ Load the salt file from the flash drive """
    if not exist(saltFileName):
        print("try to load salt but it does not exist")
        sys.exit(0)
    else:
        with open(saltFileName, "rb") as file:
            data = file.read()
        return data


def getKey(psd, salt):
    """ Generate the key with the salt and the password """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(psd))


def encrypt(data, encryptionKey):
    """ Encode the given data """
    key = getKey(encryptionKey, loadSalt())
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(data, encryptionKey):
    """ Decode the given data """
    key = getKey(encryptionKey, loadSalt())
    f = Fernet(key)
    return f.decrypt(data)


def exist(location):
    """ Check if the file at location exist """
    return os.path.exists(location)


def decodeGen(psd, fichier):
    with open(fichier, "rb") as file:
        crypted = file.read()
    try:
        data = decrypt(crypted, psd)
        k = getKey(psd, loadSalt())
        with open(fichier, 'wb') as file:
            file.write(data)
    except InvalidToken:
        print("     *****     Invalid password     *****     ")
        sys.exit(0)


def encodeGen(psd, fichier):
    with open(fichier, "rb") as file:
        decrypted = file.read()
    data = encrypt(decrypted, psd)
    k = getKey(psd, loadSalt())
    with open(fichier, 'wb') as file:
        file.write(data)


def askPasswordForKey():
    """ Ask for the decode password """
    temp = ""
    check = "check"
    counter = 0
    while (temp != check and counter < 3):
        if (counter != 0):
            print("\n*****     The two password are different     *****\n")
        print(" * Enter an encoding password * ")
        temp = getpass.getpass()
        print("\n * Type it again * ")
        check = getpass.getpass()
        counter += 1
    if (temp == check):
        return temp.encode()
    else:
        sys.exit(0)


def main():
    if not exist(saltFileName):
        print("cant find the salt file")
    elif len(sys.argv) == 3:
        fichier = sys.argv[2]
        if not exist(fichier):
            print("the file %s doesn't exist" % fichier)
            sys.exit(0)
        if sys.argv[1] == "decode":
            print(" * Enter the decoding password * ")
            psd = getpass.getpass()
            decodeGen(psd.encode(), fichier)
        elif sys.argv[1] == "encode":
            psd = askPasswordForKey()
            encodeGen(psd, fichier)
        else:
            raise ValueError("Invalid argument")
    else:
        raise ValueError("invalid argument")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Au revoir")
        sys.exit(0)
