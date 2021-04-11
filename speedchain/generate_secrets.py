from cryptography.fernet import Fernet
import os

def key_generator():
    key = Fernet.generate_key()
    if os.path.exists("./secret.key"):
        aw = input("Existing key found, do you want to overwrite it ?")
        if aw != "yes":
            return
    with open("./secret.key", "wb") as key_file:
        key_file.write(key)

if __name__ == "__main__":
    key_generator()