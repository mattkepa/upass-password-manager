import bcrypt
from services import connect_db
from utils import console, console_clear

if __name__ == '__main__':
    # Connect to database
    try:
        db = connect_db()
        cursor = db.cursor()
    except Exception:
        console.print('DatabaseError: connection with database failed', style='red')
        if db is not None:
            db.close()
        exit()

    console_clear()
    console.print('uPass - Password Manager'.center(36), style='bold')
    print('+++ Create an Account +++'.center(36))
    print('=' * 36)

    # Get and check validity of username from user
    is_valid_username = False
    while not is_valid_username:
        username = input('Username: ')
        # check if username is available
        cursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE username = %s);', (username,))
        db.commit()
        response = cursor.fetchone()
        if response[0] == False:
            is_valid_username = True
        else:
            console.print('User already exists. Please choose a different name.', style='red')

    # Get password from user
    passwords_match = False
    while not passwords_match:
        password = input('Password: ')
        password_confirm = input('Confirm password: ')
        if password == password_confirm:
            passwords_match = True
        else:
            console.print('Passwords do not match. Try again', style='red')

    # Generate hash and salt for password
    salt = bcrypt.gensalt()
    pass_bytes = bytes(password, 'utf-8')
    pass_hash = bcrypt.hashpw(pass_bytes, salt)

    # Store new user in database
    try:
        query = 'INSERT INTO users(username, password_hash, salt) VALUES (%s, %s, %s)'
        data = (username, pass_hash.decode('utf-8'), salt.decode('utf-8'))
        cursor.execute(query, data)
        db.commit()
    except Exception:
        console.print('Error: Something went wrong. Please try again later', style='red')
        if cursor:
            cursor.close()
        if db is not None:
            db.close()
        exit()

    # Output success message
    print('-' * 36)
    console.print('[green][+][/green] Account created successfully!')

    # Close db connection
    cursor.close()
    db.close()