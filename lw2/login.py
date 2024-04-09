import hashlib
import getpass
from getpass import GetPassWarning
from Crypto.Random import get_random_bytes
import logging
import argparse
import pandas as pd
import os
import subprocess

CSV_FILE_PATH = "usernames.csv"
SALT_SIZE = 16

def init():
   logging.basicConfig(level=logging.INFO)

def parse_args():
   parser = argparse.ArgumentParser(description='User login.')
   parser.add_argument('username', type=str, help="Username")
   args = parser.parse_args()
   return args
    
def get_password(new=False):
   if new:
      password = getpass.getpass("New password: ")
      repeated_password = getpass.getpass("Repeat new password: ")
      if password != repeated_password:
         return None 
      return password    
   else:
      password = getpass.getpass("Password: ")
      return password

def login(username):
    csv_file = pd.read_csv(CSV_FILE_PATH)

    for attempt in range(3):  # Allow up to three attempts
        password = get_password(new=False)
        valid_login = False  # Flag to track if login is successful

        for index, row in csv_file.iterrows():
            if row['Username'] == username:
                stored_salt = bytes.fromhex(row['Salt'])
                stored_hashed_password = row['Hashed_Password']

                entered_password_bytes = password.encode('utf-8')
                hashed_password = hashlib.sha512(entered_password_bytes + stored_salt).hexdigest()
                
                if hashed_password == stored_hashed_password:
                    if row['Force_Pass'] == 1:
                        try:
                            new_password = get_password(new=True)
                            salt = get_random_bytes(SALT_SIZE)
                            new_user_password_bytes = new_password.encode('utf-8')
                            hashed_new_password = hashlib.sha512(new_user_password_bytes + salt).hexdigest()
                            csv_file.at[index, "Salt"] = salt.hex()
                            csv_file.at[index, "Hashed_Password"] = hashed_new_password
                            csv_file.at[index, "Force_Pass"] = 0
                            csv_file.to_csv(CSV_FILE_PATH,index=False)
                        except GetPassWarning as e:
                            logging.error(f"Invalid password, error: {e}")
                    valid_login = True  
                    break

        if valid_login:
            subprocess.call('cmd.exe', shell=True)
            return  

        print("Username or password incorrect.")

    print("Maximum login attempts exceeded.")
      

def main():
   args = parse_args()
   init()
   login(args.username)
   
if __name__ == "__main__":
    main()
