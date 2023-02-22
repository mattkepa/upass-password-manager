import psycopg2
from config import db_config
from utils import console, generate_random_password, encrypt_password


def connect_db():
    """
    Connects to database and returns connection object
    """
    conn = None
    try:
        params = db_config()
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        console.print(error, style='red')

    return conn


def add_entry(db_conn, user, key):
    """
    Gets site/app name, username (or email)
    password (if user skip this program will generete it for him)
    and site url (optional) from user and store it in database
    """
    try:
        cursor = db_conn.cursor()
    except Exception:
        console.print('Error: Something went wrong. Please try again later', style='red')
        print()
        input('Press ENTER to continue...  ')
        return

    # Get site/app name from user
    while True:
        app_name = input('Site/app name:  ')
        if len(app_name) == 0:
            console.print('Field cannot be empty', style='red')
            continue
        else:
            break

    # Get email from user
    while True:
        email = input('E-mail:  ')
        if len(email) == 0:
            console.print('Field cannot be empty', style='red')
            continue
        # check if account with this app and email exists in db
        try:
            cursor.execute('SELECT EXISTS(SELECT 1 FROM entries WHERE email = %s AND site_name = %s AND user_id = %s);', (email, app_name, user['uid']))
            db_conn.commit()
            response = cursor.fetchone()
        except Exception:
            console.print('Error: Something went wrong. Please try again later', style='red')
            if cursor:
                cursor.close()
            print()
            input('Press ENTER to continue...  ')
            return

        if response[0] == False:
            break
        else:
            console.print('Entry for this app/site and email already exists. Please choose a different email.', style='red')

    # Get password from user. If blank automatically generate one for him
    while True:
        password = input('Password (skip to automatically generate):  ')
        if len(password) == 0:
            password = generate_random_password()
            break
        elif 0 < len(password) < 12:
            console.print('Password must contain at least 12 characters', style='red')
        else:
            break

    # Get site url form user (optional)
    site_url = input('Site URL (optional):  ')


    # Encrypt password
    encrypted_data = encrypt_password(password, key)

    # Add entry to db
    try:
        if site_url:
            query = 'INSERT INTO entries(site_name, email, password, site_url, user_id) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(query, (app_name, email, encrypted_data, site_url, user['uid']))
        else:
            query = 'INSERT INTO entries(site_name, email, password, user_id) VALUES (%s, %s, %s, %s)'
            cursor.execute(query, (app_name, email, encrypted_data, user['uid']))
        db_conn.commit()
        cursor.close()
    except Exception:
        console.print('Error: Something went wrong. Please try again later', style='red')
        if cursor:
            cursor.close()
        print()
        input('Press ENTER to continue...  ')
        return

    print('-' * 36)
    console.print('[green][+][/green] Entry successfully added')
    print()
    input('Press ENTER to continue...  ')


def get_entries(db_conn, user):
    """
    Fetches list of entries for current user
    """
    try:
        cursor = db_conn.cursor()
        query = 'SELECT site_name, email, site_url FROM entries WHERE user_id=%s;'
        cursor.execute(query, (user['uid'],))
        db_conn.commit()
        response = cursor.fetchall()
        cursor.close()
    except Exception:
        console.print('Error: Something went wrong. Please try again later', style='red')
        if cursor:
            cursor.close()
        print()
        input('Press ENTER to continue...  ')
        return

    return response