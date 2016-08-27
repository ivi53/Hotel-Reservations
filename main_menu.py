import os
import database_hotel
import clients
import administrators
import getpass


def clear():
    return lambda: os.system('cls')


def main():
    """
    This function is where the program begins.
    It is the general menu for the hotel. 
    """
    clear()
    print("Welcome. This is Summer Square Hotel\n")
    while True:
        print("\nWhat may we offer you today?\n")
        print("1. View our rooms")
        print("2. Look at our prices")
        print("3. Check out the discounts")
        print("4. Login")
        print("5. Register")
        print("6. Exit")
        choice = input("Option: ")
        choice = int(choice)
        if choice == 1:
            clients.view_rooms()
        elif choice == 2:
            clients.check_prices()
        elif choice == 3:
            clients.check_discounts()
        elif choice == 4:
            login()
        elif choice == 5:
            register()
        elif choice == 6:
            exit()
        else:
            print("Wrong input\n")


def register():
    """
    This function makes a new record in the clients table
    by regestering new clients.
    """
    clear()
    while True:
        username = input("Username: ")
        username = str(username)
        if database_hotel.is_username_free(username):
            name = input("Full name: ")
            name = str(name)
            email = input("Email: ")
            email = str(email)
            password = getpass.getpass()
            address = input("Address: ")
            address = str(address)
            ucn = input("UCN: ")
            ucn = str(ucn)
            visits = 0
            card_num = input("Card number: ")
            card_num = str(card_num)
            security = input("Security number: ")
            security = str(security)
            expiration = input("Expiration date(MM-YYYY): ")
            expiration = str(expiration)
            database_hotel.add_client(username, password, email, name,
                                      address, ucn, visits, card_num,
                                      security, expiration)
            text = """Good day, {},\n
                   You just registered in Summer Square Hotel\n
                   Your username: {}\n
                   Your password: {}\n
                   Hope you enjoy our hotel.\n
                   Have a nice day! :)""".format(name, username, password)
            print("A confirmation email will be sent soon.\n")
            clients.send_email(email, text)
            return
        else:
            print("Username {} is already taken.".format(username) +
                  "Please choose another one or quit.\n")
            choice = input("Do you want to quit?(y/n): ")
            if choice == 'y':
                exit()
            else:
                pass


def login():
    """
    This function leads to the different parts of the menus
    depending on what role the user is given.
    """
    clear()
    while True:
        username = input("Username: ")
        username = str(username)
        password = getpass.getpass()
        if database_hotel.is_username_free(username) and\
           database_hotel.is_admin_free(username):
            print("You don't have a registration yet")
            choice = input("Do you want to make one?(y/n): ")
            if choice != 'y':
                return
            register()
        else:
            if database_hotel.admin_pass(username, password) or\
               database_hotel.check_password(username, password):
                table = database_hotel.client_or_admin_login(username)
                if table == 'client':
                    clients.menu(username)
                    exit()
                elif table == 'admin':
                    administrators.menu(username)
                    exit()
                else:
                    exit()
            else:
                print("Wrong password!")
                choice = input("Do you want yo quit?(y/n): ")
                if choice == 'y':
                    exit()

if __name__ == '__main__':
    main()
