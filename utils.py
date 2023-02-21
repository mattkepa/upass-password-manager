import os
from rich.console import Console


console = Console()


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
    console.print('  [red][0][/red] -- Exit')
    console.print('-' * 36)


def console_clear():
    """
    Clears console window
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')