from cryptography.fernet import Fernet
from database import *

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    try:
        f = open("secret.key", "rb").read()
        return f
    except:
        generate_key()
        return open("secret.key", "rb").read()

def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    #print(encrypted_message)
    return encrypted_message

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    #print(decrypted_message.decode())
    return decrypted_message.decode()

# from cryptography.fernet import Fernet
# from database import *
# import base64
#
# def load_key():
#     """
#     Loads the key named `secret.key` from the current directory.
#     """
#     cursor.execute("SELECT password FROM masterkey WHERE id=1")
#     # print(checkHashedPassword)
#     return cursor.fetchall()[0][0]
#
#     '''if not load_key():
#         def generate_key():
#             """
#             Generates a key and save it into a file
#             """
#             key = Fernet.generate_key()
#             with open("secret.key", "wb") as key_file:
#                 key_file.write(key)
#             #print(key)
#         generate_key()'''
#
# def encrypt_message(string):
#     """
#     Encrypts a message
#     """
#     key = load_key()
#     encoded_chars = []
#     for i in range(len(string)):
#         key_c = key[i % len(key)]
#         encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
#         encoded_chars.append(encoded_c)
#     encoded_string = "".join(encoded_chars)
#     return base64.urlsafe_b64encode(encoded_string)
#
#     '''key = load_key()
#     encoded_message = message.encode()
#     f = Fernet(key)
#     encrypted_message = f.encrypt(encoded_message)
#
#     #print(encrypted_message)
#     return encrypted_message'''
#
# def decrypt_message(encrypted_message):
#     """
#     Decrypts an encrypted message
#     """
#     key = load_key()
#     f = Fernet(key)
#     decrypted_message = f.decrypt(encrypted_message)
#
#     #print(decrypted_message.decode())
#     return decrypted_message.decode()
#
# #a = encrypt_message("abcd")
# #print(a)
# #decrypt_message
# print(load_key())
#
# encrypt_message("HI")
# '''
# def encode(key, string):
#     encoded_chars = []
#     for i in xrange(len(string)):
#         key_c = key[i % len(key)]
#         encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
#         encoded_chars.append(encoded_c)
#     encoded_string = "".join(encoded_chars)
#     return base64.urlsafe_b64encode(encoded_string)
# '''
