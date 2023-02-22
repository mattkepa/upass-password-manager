import bcrypt
from Crypto.Protocol.KDF import PBKDF2
from getpass import getpass
from services import connect_db, add_entry, get_entries, get_password
from utils import console, display_menu, display_entries, console_clear


#
# Connect to db
try:
    db = connect_db()
    cursor = db.cursor()
except Exception:
    console.print('DatabaseError: connection with database failed', style='red')
    if db is not None:
        db.close()
        db = None
    exit()


#
# User authentication
console_clear()
console.print('uPass - Password Manager'.center(36), style='bold')
print('### Unlock Database ###'.center(36))
print('=' * 36)

user = {}
authenticated = False
while not authenticated:
    username = input('Username: ')
    password = getpass('Password: ')

    if len(username) == 0 or len(password) == 0:
        console.print('Username and password fields cannot be empty.', style='red')
        continue

    try:
        cursor.execute('SELECT * FROM users WHERE username = %s;', (username,))
        db.commit()
        response = cursor.fetchone()
    except Exception:
        console.print('Error: Something went wrong. Please try again later', style='red')
        cursor.close()
        db.close()
        db = None
        exit()

    if response is not None:
        valid_credentials = bcrypt.checkpw(bytes(password, 'utf-8'), bytes(response[2], 'utf-8'))
        if valid_credentials:
            user = {
                'uid': response[0],
                'username': response[1],
                'password_hash': bytes(response[2], 'utf-8'),
                'salt': bytes(response[3], 'utf-8')
            }
            authenticated = True
            cursor.close()
        else:
            console.print('Invalid username or password.', style='red')
    else:
        console.print('Invalid username or password.', style='red')

#
# Generate key for encryption and decryption
key = PBKDF2(password, user['salt'], dkLen=32)


#
# Main program loop
console_clear() # clear console after sucessfull authentication
while True:
    display_menu()
    choice = input('Choose an option:  ')
    print('-' * 36)
    print()

    if choice == '1':
        console_clear()
        print('+++ Create new entry +++'.center(36))
        print('=' * 36)
        add_entry(db, user, key)
        console_clear()
    elif choice == '2':
        console_clear()
        console.print('\tEntries', style='bold')
        print('=' * 36)
        entries = get_entries(db, user)
        display_entries(entries)
        console_clear()
    elif choice == '3':
        console_clear()
        print('*** Get Password ***'.center(36))
        print('=' * 36)
        get_password(db, user, key)
        console_clear()
    elif choice == '0':
        console_clear()
        break
    else:
        console.print('Incorrect option selected', style='red')
        print()


#
# Close db connection
if db is not None:
    db.close()