# Password Manager README

## System Description

This system includes two tools: a user management script (`usergmt.py`) and a login script (`login.py`). Both tools worktogether to manage and authenticate user credentials. The user management script allows for adding, modifying, and deleting user credentials, while the login script handles user authentication.

### User Management Script (usergmt.py)

- **Add User**: Adds a new user with a username and password.
- **Change Password**: Changes the password for an existing user.
- **Force Password Change**: Flags a user to change their password upon next login.
- **Delete User**: Removes a user from the system.

### Login Script (login.py)

- Handles user authentication.
- Allows three attempts to enter the correct password.
- If the password must be changed (`Force_Pass`), prompts the user to do so.
- Opens a Command Prompt upon successful authentication.

## Security Features

- Passwords are hashed with SHA-512 algorithm and salted using `get_random_bytes` from the Crypto library.
- Salt is a 16-byte randomly generated value, enhancing security.
- No indication is given as to whether a username is incorrect or the password does not match, for security purposes.
- A maximum of three attempts is allowed for user authentication.

## How to Use

### User Management

1. **Add a New User**:
   ```bash
   python usergmt.py add [username]

2. **Change a User's Password**:
   ```bash
   python usergmt.py passwd [username]
   
3. **Force a User to Change Password on Next Login**:
   ```bash
   python usergmt.py forcepass [username]

4. **Delete a User**:
   ```bash
   python usergmt.py del [username]

### User Login
**To login as a user run**: 
   ```bash
   python login.py [username]