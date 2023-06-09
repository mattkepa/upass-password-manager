import os
import random
import string
from Crypto.Cipher import AES
from tabulate import tabulate
from rich.console import Console


console = Console()


def encrypt_password(data, key):
    """
    Enctypts password with given key and returns encrypted data in bytes array with IV in first 16 bytes

    :param: data: str - data (password) to encrypt
    :param: key: bytes - hash key to encrypt/decrypt password
    """
    cipher = AES.new(key, AES.MODE_CFB)
    iv = cipher.iv
    encrypted_password = cipher.encrypt(bytes(data, 'utf-8'))
    encrypted_data = iv + encrypted_password    # add Initialization Vector to 16 first bytes of enctypted password
    return encrypted_data


def decrypt_password(data, key):
    """
    Decrypts password with given key and returns plain text password

    :param: data: bytes - data (password) to decrypt
    :param: key: bytes - hash key to encrypt/decrypt password
    """
    IV = data[:16] # extract Initialization Vector from 16 first bytes of enctypted password
    encrypted_pass = data[16:] # extract encrypted password from the rest of encrypted stored data

    cipher = AES.new(key, AES.MODE_CFB, iv=IV)
    decrypted_password = cipher.decrypt(encrypted_pass).decode('utf-8')
    return decrypted_password


def generate_random_password(length=18):
    """
    Generates random password from set of letters, digits and psecial characters
    with specified length (default is 18)

    :param length: int - length of password (default is 18)
    """
    random_source_set = string.ascii_letters + string.digits + '!@#$%^&(){}[]-_'

    password_chars = []
    password_chars.append(random.choice(string.ascii_lowercase)) # select 1 lowercase
    password_chars.append(random.choice(string.ascii_uppercase)) # select 1 upperrcase
    password_chars.append(random.choice(string.digits)) # select 1 digit
    password_chars.append(random.choice('!@#$%^&(){}[]-_')) # select 1 special character

    # generate other remaining characters
    for _ in range(length - 4):
        password_chars.append(random.choice(random_source_set))

    # shuffle all characters
    random.shuffle(password_chars)

    password = ''.join(password_chars)
    return password


def display_menu():
    """
    Displays main menu to user
    """
    console.print('uPass - Password Manager'.center(36), style='bold')
    console.print('-' * 36)
    console.print(('-' * 15) + ' [bold]MENU[/bold] ' + ('-' * 15))
    console.print('  [green][1][/green] -- Add new entry')
    console.print('  [cyan][2][/cyan] -- Show user\'s apps/sites')
    console.print('  [cyan][3][/cyan] -- Get password for app/site')
    console.print('  [orange1][4][/orange1] -- Delete entry for app/site')
    console.print('  [red][0][/red] -- Exit')
    console.print('-' * 36)


def display_entries(data):
    """
    Displays list of entries in read-friendly table form

    :param data: list - entries retered from database
    """
    headers = ['Site/App Name', 'E-mail', 'Site URL']

    if not data:
        print('+' + '-' * 34 + '+')
        print('|' + ' You don\'t have any entries yet'.ljust(34) + '|')
        print('+' + '-' * 34 + '+')
    else:
        print(tabulate(data, headers=headers, tablefmt='grid'))

    print()
    input('Press ENTER to continue...  ')


def console_clear():
    """
    Clears console window
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')