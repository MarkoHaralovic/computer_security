#jednostavan i siguran prototip alata za pohranu zaporki (password manager) koristeći simetričnu kriptografiju

#  Alat mora omogućavati korisniku sljedeće:
# 1. Inicijalizacija alata odnosno stvaranje prazne baze zaporki.
# 2. Pohrana para adresa, zaporka. Ako je već pohranjena zaporka pod istom adresom onda ju je potrebno zamijeniti sa zadanom.
# 3. Dohvaćanje pohranjene zaporke za zadanu adresu.

#  potrebno je osigurati sljedeć sigurnosne zahtjeve:
# 1. Povjerljivost zaporki: napadač ne može odrediti nikakve informacije o zaporkama, čak niti njihovu
# duljinu, čak ni jesu li zaporke za dvije adrese jednake, čak ni je li nova zaporka jednaka staroj kada
# se promijeni.
# 2. Povjerljivost adresa: napadač ne može odrediti nikakve informacije o adresama, osim da zna
# koliko se različitih adresa nalazi u bazi.
# 3. Integritet adresa i zaporki: nije moguće da korisnik dobije od alata zaporku za određenu adresu,
# ako prethodno nije unio točno tu zaporku za točno tu adresu. Obratite pažnju na napad zamijene:
# napadač ne smije moći zamijeniti zaporku određene adrese zaporkom neke druge adrese.

#The Crypto.Cipher package contains algorithms for protecting the confidentiality of data.
# Symmetric ciphers: all parties use the same key, for both decrypting and encrypting data. 
# Symmetric ciphers are typically very fast and can process very large amount of data.

import os  
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import logging
import argparse

logging.basicConfig(level=logging.INFO) 

FILE_NAME = 'encrypted_passwords.bin'
SALT_SIZE = 16 #16 bajtova
IV_SIZE = 16  # 16 bajtova
KEY_ITERATIONS = 1000000
KEY_SIZE = 32 #256 bitova
VERIFICATION_TOKEN = b'verify'



def initialize_database(master_password):
    if os.path.isfile("encrypted_passwords.bin"):
        os.remove("encrypted_passwords.bin")
        logging.info("Database already exists, and it will be overwritten")

    salt = get_random_bytes(SALT_SIZE)
    iv = get_random_bytes(IV_SIZE)
    key = derive_key(master_password, salt)

    verification_token_encrypted, verification_tag = encrypt_data(VERIFICATION_TOKEN, key, iv)

    data = b''
    ciphertext, tag = encrypt_data(data, key, iv)
    
    with open(FILE_NAME, 'wb') as file:
        file.write(iv)
        file.write(salt)
        file.write(verification_token_encrypted)
        file.write(verification_tag)
        file.write(ciphertext)
        file.write(tag)

def is_master_password_correct(master_password):
    try:
        iv, salt, verification_token_encrypted, verification_tag = load_encrypted_data(FILE_NAME, master_password, only_check=True)
        key = derive_key(master_password, salt)
        decrypted_verification_token = decrypt_data(verification_token_encrypted, key, iv, verification_tag)
        if decrypted_verification_token is None:
            return False
        logging.warning(f"decrypted_verification_token : {decrypted_verification_token}")
        logging.warning(decrypted_verification_token == VERIFICATION_TOKEN)
        return decrypted_verification_token == VERIFICATION_TOKEN
    except Exception as e:
        logging.error(f"Error during master password verification: {e}")
        return False
 
def load_encrypted_data(filename, master_password, only_check=False):
    with open(filename, 'rb') as file:
        iv = file.read(IV_SIZE)
        salt = file.read(SALT_SIZE)
        
        if only_check:
            verification_token_encrypted = file.read(len(VERIFICATION_TOKEN))
            verification_tag = file.read(AES.block_size) 
            return iv, salt, verification_token_encrypted, verification_tag

        ciphertext = file.read(-1)

    key = derive_key(master_password, salt)

    try:
        decrypted_data = decrypt_data(ciphertext, key, iv)
        return iv, salt, decrypted_data, True  
    except Exception as e:
        return iv, salt, None, False

def parse_data(data_string):
    data_dict = {}
    for line in data_string.split('\n'):
        if line:
            address, password = line.split(',')
            data_dict[address] = password
    return data_dict

def format_data(data_dict):
    return '\n'.join([f"{address},{password}" for address, password in data_dict.items()]).encode('utf-8')
 
def save_password(master_password, address, new_password):
    # Check if master password is correct
    if not is_master_password_correct(master_password):
        logging.error("Master password is incorrect.")
        return False
    else:
        logging.info("Master password is correct.")

    # Attempt to load existing data
    iv, salt, existing_data, success = load_encrypted_data(FILE_NAME, master_password, only_check=False)
    logging.info(f"IV: {iv}")
    logging.info(f"Salt: {salt}")
    logging.info(f"Existing Data: {existing_data}")
    logging.info(f"Success: {success}")

    # if not success:
    #     logging.error("Failed to load existing data or master password incorrect.")
    #     return False

    # Parse existing data and update with new password
    data_dict = {}
    if existing_data:
        try:
            data_dict = parse_data(existing_data.decode('utf-8'))
        except UnicodeDecodeError as e:
            logging.error(f"Error decoding existing data: {e}")
            return False
    data_dict[address] = new_password

    # Encrypt and save the updated data
    data_string = format_data(data_dict)
    key = derive_key(master_password, salt)
    ciphertext, tag = encrypt_data(data_string, key, iv)

    with open(FILE_NAME, 'wb') as file:
        file.write(iv)
        file.write(salt)
        file.write(ciphertext)
        file.write(tag)

    logging.info(f"Stored password for {address}.")
    return True
def get_password(master_password, address):
    iv, salt, decrypted_data, success = load_encrypted_data(FILE_NAME, master_password)
    if decrypted_data is None:
        logging.info("Master password incorrect or integrity check failed.")
        return None
    
    data_dict = parse_data(decrypted_data.decode('utf-8'))
    return data_dict.get(address)


def encrypt_data(data, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, tag
   
def decrypt_data(ciphertext, key, iv, tag):
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data
    except ValueError:
        return None
    
def derive_key(password, salt, iterations=KEY_ITERATIONS, key_size=KEY_SIZE):
    """
    Funkcija za derivaciju ključa iz zaporke koristeći PBKDF2.
    """
    key = PBKDF2(password, salt, dkLen=key_size, count=iterations)
    return key

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
        logging.info('Password manager initialized.')
    elif args.command == 'put':
        save_password(args.master_password, args.address, args.password)
        logging.info(f'Stored password for {args.address}.')
    elif args.command == 'get':
        password = get_password(args.master_password, args.address)
        if password:
            logging.info(f'Password for {args.address} is: {password}')
        else:
            logging.info(f'Master password incorrect or integrity check failed.')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()