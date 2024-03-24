import os  
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import logging
import argparse
import sys
import pickle

logging.basicConfig(level=logging.INFO) 

FILE_NAME = 'encrypted_passwords.bin'
SALT_SIZE = 16 #16 bytes
IV_SIZE = 16  # 16 bytes
TAG_SIZE=16
KEY_ITERATIONS = 1000000
KEY_SIZE = 32 #256 bits

def derive_key(password, salt, iterations=KEY_ITERATIONS, key_size=KEY_SIZE):
    key = PBKDF2(password, salt, dkLen=key_size, count=iterations)
    return key
def encrypt_data(data, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    return cipher.encrypt_and_digest(data)
def decrypt_data(ciphertext, key, iv, tag):
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        return  cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError as e:
        logging.error(f"Master password incorrect or integrity check failed. ")
        sys.exit(1)
def serialize_data(data_dict):
    return pickle.dumps(data_dict) if data_dict is not None else None

def deserialize_data(data_bytes):
    return pickle.loads(data_bytes)  if data_bytes is not None else None

def initialize_database(master_password):
    if os.path.isfile(FILE_NAME):
        logging.info("Database already exists, and it will be overwritten")
    os.remove(FILE_NAME) if os.path.exists(FILE_NAME) else None
    salt = get_random_bytes(SALT_SIZE)
    iv = get_random_bytes(IV_SIZE)
    empty_data = {}
    serialized_data = serialize_data(empty_data)
    key = derive_key(master_password, salt)
    ciphertext, tag = encrypt_data(serialized_data, key, iv)
    with open(FILE_NAME, 'wb') as file:
        file.write(salt)
        file.write(iv)
        file.write(tag)
        file.write(ciphertext)
    logging.info('Password manager initialized.')
    
def load_decrypted_data(filename, master_password):
    with open(filename, 'rb') as file:
        salt = file.read(SALT_SIZE)
        iv = file.read(IV_SIZE)   
        tag = file.read(TAG_SIZE)
        encrypted_data = file.read()

    key = derive_key(master_password, salt)
    decrypted_data = decrypt_data(encrypted_data, key, iv, tag)
    return iv, salt, decrypted_data

def save_password(master_password, address, new_password):
    iv,salt,decrypted_data= load_decrypted_data(FILE_NAME,master_password) 
    data = deserialize_data(decrypted_data)
    data[address] = new_password
    serialized_data = serialize_data(data)
    key=derive_key(master_password, salt)
    ciphertext, tag = encrypt_data(serialized_data, key, iv)
    with open(FILE_NAME, 'wb') as file:
        file.write(salt)
        file.write(iv)
        file.write(tag)
        file.write(ciphertext)
    logging.info(f"Stored password for {address}.")
    return True

def get_password(master_password, address):
    _,_,decrypted_data= load_decrypted_data(FILE_NAME, master_password)
    data=deserialize_data(decrypted_data)
    return data.get(address)

def main():
    parser = argparse.ArgumentParser(description='Password Manager')
    subparsers = parser.add_subparsers(dest='command')

    parser_init = subparsers.add_parser('init', help='Initialize the password database')
    parser_init.add_argument('master_password', type=str, help='Master password for the password manager')

    parser_put = subparsers.add_parser('put', help='Store a password')
    parser_put.add_argument('master_password', type=str, help='Master password for the password manager')
    parser_put.add_argument('address', type=str, help='Website or service address')
    parser_put.add_argument('password', type=str, help='Password to store')

    parser_get = subparsers.add_parser('get', help='Retrieve a stored password')
    parser_get.add_argument('master_password', type=str, help='Master password for the password manager')
    parser_get.add_argument('address', type=str, help='Website or service address')

    args = parser.parse_args()

    if args.command == 'init':
        initialize_database(args.master_password)
    elif args.command == 'put':
        save_password(args.master_password, args.address, args.password)
    elif args.command == 'get':
        password = get_password(args.master_password, args.address)
        logging.info(f'Password for {args.address} is: {password}')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()