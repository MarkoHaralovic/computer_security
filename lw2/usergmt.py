import hashlib
import getpass
from getpass import GetPassWarning
import logging
from Crypto.Random import get_random_bytes
import argparse
import pandas as pd
import os

CSV_FILE_PATH = "usernames.csv"
SALT_SIZE = 16


def init():
   logging.basicConfig(level=logging.INFO)
   if not os.path.exists(CSV_FILE_PATH):
      df = pd.DataFrame()
      df = pd.DataFrame(columns=['Username', 'Salt', 'Hashed_Password', 'Force_Pass'])
      df.to_csv(CSV_FILE_PATH,index=False)
            
def parse_args():
   parser = argparse.ArgumentParser(description='User Admin')
   parser.add_argument('task',type=str,choices=['add','passwd','forcepass','del'],help="Type of task to run")
   parser.add_argument('username', type=str, help="Username")
   args = parser.parse_args()
   return args
    
def get_password():
   password = getpass.getpass("Password: ")
   repeated_password = getpass.getpass("Repeat Password: ")
   if password != repeated_password:
      return None
   return password    

def add(username):
    try:
        user_password = get_password()
    except GetPassWarning:
        logging.error("Please input a valid username.")
        return
    if user_password is None:
        logging.error("User add failed. Password mismatch.")
        return
    user_password_bytes = user_password.encode('utf-8')
    salt = get_random_bytes(SALT_SIZE)
    hashed_password = hashlib.sha512(user_password_bytes + salt).hexdigest()

    csv_file = pd.read_csv(CSV_FILE_PATH)
   
    if username not in csv_file['Username'].values:
        new_user_df = pd.DataFrame([[username, salt.hex(), hashed_password, 0]], 
                                   columns=['Username', 'Salt', 'Hashed_Password', 'Force_Pass'])

        csv_file = pd.concat([csv_file, new_user_df], ignore_index=True)
        csv_file.to_csv(CSV_FILE_PATH, index=False)
        logging.info(f"User {username} successfully added.")
    else:
        logging.info(f"User {username} already exists.")


def passwd(username):
   try:
      new_user_password = get_password()
   except GetPassWarning():
      logging.error("Please input a valid username.")
      return
   
   if new_user_password is None:
      logging.error("Password change failed. Password mismatch.")
      return
   
   csv_file = pd.read_csv(CSV_FILE_PATH)
   
   if csv_file['Username'].str.contains(username).any():
      salt = get_random_bytes(SALT_SIZE)
      new_user_password_bytes = new_user_password.encode('utf-8')
      hashed_password = hashlib.sha512(new_user_password_bytes + salt).hexdigest()
      csv_file.loc[csv_file['Username'] == username, ["Salt", "Hashed_Password", "Force_Pass"]] = [salt.hex(), hashed_password, 0]
      csv_file.to_csv(CSV_FILE_PATH,index=False)
      logging.info(f"Password change successful.")
      return 
   logging.warning(f"Password change failed.")
   return 

def forcepass(username):
   csv_file = pd.read_csv(CSV_FILE_PATH)
   if csv_file['Username'].str.contains(username).any():
      csv_file.loc[csv_file['Username'] == username, ['Force_Pass']] = [int(1)]
      csv_file.to_csv(CSV_FILE_PATH,index=False)
      logging.info(f"User {username} will be requested to change password on next login.")
      return 
   logging.warning(f"User not found.")
   return 

def deletion(username):
    csv_file = pd.read_csv(CSV_FILE_PATH)
    if csv_file['Username'].str.contains(username).any():
       csv_file = csv_file[csv_file['Username']!=username]
       csv_file.to_csv(CSV_FILE_PATH,index=False)
       logging.info(f"User {username} successfully removed.")
    else:
        logging.info(f"User not found.")

def main():
   args = parse_args()
   init()
   if args.task == 'add':
      add(args.username)
   elif args.task == 'passwd':
      passwd(args.username)
   elif args.task == 'del':
      deletion(args.username)
   elif args.task == 'forcepass':
      forcepass(args.username)
   else:
      raise Exception("Invalid argument passed")
   
if __name__ == "__main__":
    main()
