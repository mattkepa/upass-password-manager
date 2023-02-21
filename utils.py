import os
from rich.console import Console

console = Console()

def console_clear():
    """
    Clears console window
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')