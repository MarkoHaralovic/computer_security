# Password Manager README

## System Description

This tool is designed as a solution for securely storing user passwords. Utilizing a master password that is derived using the PBKDF2 key derivation function, it stores pairs of addresses and passwords in the database. For decryption, the tool uses both a key and a salt, which is a randomly generated 16-byte value, to enhance the password's security. The salt is produced using the `get_random_bytes` function from the Crypto library.

The database is a binary file initialized at a specified location. In cases where a file with the same name already exists at that location, it will be overwritten with a new database, and the user will be notified accordingly. Initially, the database will store the salt, an initialization vector, and an empty dictionary.

For each address, only one password can be stored. If a user submits a new password for an address that already has a stored password, the former one is overwritten. The latest password is then saved in the database.

To store a password, the master password is required. It is first derived, and then the data is encrypted using the derived key. These encrypted data are serialized and stored in the binary file, along with a 16-byte salt and an initialization vector. I used AES, which is a symmetric key algorithm, meaning it uses the same key for both encryption and decryption.

Retrieving data follows a similar process. The master password is used to access and deserialize the binary record of passwords. Subsequently, the password for the specified address can be obtained.

The system's security is robust, primarily against brute-force attacks, as neither the length of the master password nor its format is recorded. The binary data are indecipherable and cannot be decrypted without the correct master password. An incorrect password input will result in a "MAC check failed" error when employing the `decrypt_and_verify` function from the Crypto library.

## How to Use

To launch the manager, execute the following command:

```bash
python lab1.py
```


This command will display a description of the tool and the available commands.

### Initializing the Password Database
- **Command:** `init`
- **Purpose:** Initializes the password database.
- **Usage Example:** `python password_manager.py init "YourMasterPassword"`

### Storing a New Password
- **Command:** `put`
- **Purpose:** Stores a new password for a specified address.
- **Usage Example:** `python password_manager.py put "YourMasterPassword" "example.com" "YourPassword"`

### Retrieving a Stored Password
- **Command:** `get`
- **Purpose:** Retrieves a stored password for a specified address.
- **Usage Example:** `python password_manager.py get "YourMasterPassword" "example.com"`
