import os
import random
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = "(encrypted)" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = ''
    for i in range(16):
        IV += chr(random.randint(0, 0xFF))
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:

            outfile.write(filesize)
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += " " * (16 - len(chunk) %16)

                outfile.write(encryptor.encrypt(chunk))


    print "Done"




def decrypt(key, filename):
    chunksize = 64 * 1024
    outputFile ="(decrypted)" + filename[11:]


    with open(filename, 'rb') as infile:
        filesize = long(infile.read(16))
        IV = infile.read(16)


        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(filesize)

    print "Done"


def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()

def getPassword():
    getPassword = os.urandom(16)
    return getPassword + "   <----- This is your strong password! be sure to write this down somewhere safe! \n "


def Main():
    print "Welcome to the encryption program!"
    
    choice = raw_input("Would you like to [E]ncrypt or [D]ecrpyt?: ")

    
    if choice == "E":
        get_password = raw_input("Would you like us to give you a very, very strong password? [Y] [N] :  ")
        if get_password == "Y":
           got_password = os.urandom(16)
           print got_password + "   <----- This is your strong password! Be sure to keep this somewhere safe"

        elif get_password == "N":
            pass

        else:
            print "No option recognized . . ."
        filename = raw_input("File to encrypt?: ")
        if get_password == "Y":
            password = got_password
            encrypt(getKey(password), filename)
        else:
            password = raw_input("Password?: ")
            encrypt(getKey(password), filename)

    elif choice == "D":
        filename = raw_input("File to decrypt?: ")
        password = raw_input("Password?: ")
        decrypt(getKey(password), filename)
        

    else:
        print "No option selected, closing. . ."


if __name__ == '__main__':
    Main()
    
