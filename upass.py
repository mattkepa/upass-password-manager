from utils import console, display_menu

while True:
    display_menu()
    choice = input('Choose an option:  ')
    print('-' * 36)
    print()

    if choice == '1':
        print('+++ Create new entry +++'.center(36))
        print('=' * 36)
        # todo: add entry fuction
    elif choice == '2':
        console.print('Entries'.center(36), style='bold')
        print('=' * 36)
        # todo: get and display entries functions
    elif choice == '3':
        print('*** Get Password ***'.center(36))
        print('=' * 36)
        # todo: get password function
    elif choice == '0':
        break
    else:
        console.print('Incorrect option selected', style='red')
        print()