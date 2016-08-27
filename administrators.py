import database_hotel
import os
import getpass
from prettytable import PrettyTable
import time


clear = lambda: os.system('cls')


def menu(username):
    """
    This function serves as a menu when the file is opened.
    It redirects the roles between the administrators
    @type  username: string
    @param username: the username of the administrator
    """
    clear()
    admin_info = database_hotel.get_admin_info(username)
    name = admin_info[0]
    job = admin_info[1]
    print('Good day, {}'.format(name))
    time.sleep(2)
    if job == 'receptionist':
        receptionist()
    if job == 'database admin':
        admin()
    if job == 'manager':
        manager()


def receptionist():
    """
    Available options for the receptionsists ot the hotel. 
    """
    print('What would you like to do?\n')
    while True:
        clear()
        print("1. Make a reservation")
        print("2. Cancel a reservation")
        print("3. Add a problem")
        print("4. Check a reservation")
        print("5. Exit")
        choice = input("Which option do you want?: ")
        choice = int(choice)
        if choice == 1:
            make_a_reservation(username)
        elif choice == 3:
            add_a_problem()
        elif choice == 2:
            delete_a_reservation()
        elif choice == 4:
            check_a_reservation()
        elif choice == 5:
            exit()
        else:
            print('Wrong input! Try again.\n')


def admin():
    """
    Available options for the admin of the hotel.
    """
    print('What would you like to do?\n')
    while True:
        clear()
        print("\n1. rooms")
        print("2. clients")
        print("3. administrators")
        print("4. Exit")
        table = input("Which table do you want to change?: ")
        table = int(table)
        if table == 1:
            decision =\
            input("To add a room press 'a', to delete a room press 'd': ")
            if decision == 'a':
                add_a_room()
            elif decision == 'd':
                delete_a_room()
            else:
                print("Wrong input\n")
        elif table == 2:
            delete_a_client()
        elif table == 3:
            decision =\
            input(
            "To add an administrator press 'a', to delete an administrator press 'd': "
            )
            if decision == 'a':
                add_an_administrator()
            elif decision == 'd':
                delete_an_administrator()
            else:
                print("Wrong input\n")
        elif table == 4:
            exit()
        else:
            print("Wrong input\n")


def manager():
    """
    Available options for the manager
    """
    print('What would you like to do?\n')
    while True:
        clear()
        print("1. Add a receptionist")
        print("2. Remove a receptionist")
        print("3. Update periods' prices")
        print("4. Add a room")
        print("5. Remove a room")
        print("6. Make a reservation")
        print("7. Remove a reservation")
        print("8. Update extras' prices")
        print("9. Update visits' discounts")
        print("10. Update children's discounts")
        print("11. Exit\n")
        choice = input("Option: ")
        choice = int(choice)
        if choice == 1:
            add_an_administrator('receptionist')
        elif choice == 2:
            delete_an_administrator()
        elif choice == 3:
            update_periods()
        elif choice == 4:
            add_a_room()
        elif choice == 5:
            delete_a_room()
        elif choice == 6:
            make_a_reservation(username)
        elif choice == 7:
            delete_a_reservation()
        elif choice == 8:
            update_extras()
        elif choice == 9:
            update_visits()
        elif choice == 10:
            update_children()
        elif choice == 11:
            exit()
        else:
            print("Wrong input!\n")


def update_periods():
    """
    With this function the prices of different periods can be updatedin the database.
    """
    periods = database_hotel.get_all_room_prices()
    periods_table = PrettyTable(["ID",
                                 "Begin date",
                                 "End date",
                                 "Feeding type",
                                 "Price"])
    for period in periods:
        periods_table.add_row(period)
    print(periods_table)
    choice = input("Choice one of the above periods: ")
    choice = int(choice)
    price = input("New price: ")
    price = float(price)
    database_hotel.update_room_price(choice, price)


def add_a_room():
    """
    With this function a new room can be added to the current ones in the database.
    """
    number = input("Number room: ")
    number = int(number)
    num_primary = input("Number of primary people: ")
    num_primary = int(num_primary)
    num_extra = input("Number of extra people: ")
    num_extra = int(num_extra)
    extras = input("Extras: ")
    extras = str(extras)
    database_hotel.add_room(number, num_primary, num_extra, extras)
    print("Ready!\n")
    database_hotel.conn.commit()


def delete_a_room():
    """
    With this function a certain room can be deleted from the database.
    """
    number = input("What is the room's number?: ")
    number = int(number)
    database_hotel.delete_room(number)


def delete_a_client():
    """
    With this function a certain client can be removed from the database.
    """
    client_username = input("Which client do you want to remove?: ")
    client_username = str(client_username)
    database_hotel.delete_client(client_username)


def add_an_administrator(*args):
    """
    With this function an administrator can be added to the database.
    @type *args: string
    @param *args: to hire a receptionist in particular, can be ommited
    """
    username = input("Username: ")
    username = str(username)
    while not database_hotel.is_admin_free(username):
        print("This one is occupied. Choose another one")
        username = input("Username: ")
        username = str(username)
    password = getpass.getpass()
    name = input("Full name: ")
    name = str(name)
    if not args:
        job = input("Job: ")
        job = str(job)
    else:
        job = args[0]
    database_hotel.add_administrator(username, password, name, job)
    database_hotel.conn.commit()


def delete_an_administrator():
    """
    With this function an administrator can be removed from the database.
    """
    username = input("Username: ")
    username = str(username)
    database_hotel.delete_administrator(username)


def view_all_reservations():
    """
    With this function all of the reservation can be printed on the screen.
    """
    reservations = get_all_reservations()
    reservation_table = PrettyTable(["ID",
                                     "Begin date",
                                     "End date",
                                     "Adults",
                                     "Children",
                                     "Feeding type",
                                     "Extras",
                                     "Price",
                                     "Paid"])
    for reservation in reservations:
        reservation_table.add_row(reservation)
    print(reservation_table)


def make_a_reservation(username):
    """
    With this function someone can make a reservation.
    @type username: string
    @param username: the username of the person wanting to make the reservation, can be an administrator
    """
    reservation_maker.menu(username)


def delete_a_reservation():
    """
    With this function a reservation can be removed from the database.
    """
    view_all_reservations()
    id_reservation = input("Which one do you want to delete?: ")
    id_reservation = int(id_reservation)
    database_hotel.delete_reservation(id_reservation)


def add_a_problem():
    """
    With this function a problem can be added to a reservation.
    """
    room = input("Which room has a problem?: ")
    room = int(room)
    person = input("Who occupied the room?: ")
    person = str(person)
    id_reservation =\
    database_hotel.get_current_reservation_id_from_name(person, room)
    problems = input("What is the problem?: ")
    problems = str(problems)
    problem_cost = input("How much does the it cost?: ")
    problem_cost = float(problem_cost)
    database_hotel.add_problems(id_reservation, problems, problmes_cost)
    choice = input("Anything else?(y/n) ")


def check_a_reservation():
    """
    With this function a certain reservation can be printed on the screen.
    """
    id_res = input("Which reservation?: ")
    id_res = int(id_res)
    info = database_hotel.get_reservation_info(id_res)
    info_table = PrettyTable(["Begin date",
                              "End date",
                              "Adults",
                              "Children",
                              "Feeding type",
                              "Extras",
                              "Price",
                              "Paid"])
    for piece in info:
        info_table.add_row(piece)
    print(info_table)


def update_extras():
    """
    With this function the price of particular extra
    can be changed in the database.
    """
    extras = database_hotel.get_all_extras()
    extras_table = PrettyTable(["ID",
                               "Extra",
                                "Price"])
    for extra in extras:
        extras_table.add_row(extra)
    print(extras_table)
    extra_id = input("Which extra do you want to change?: ")
    extra_id = int(extra_id)
    price = input("New price: ")
    price = float(price)
    database_hotel.update_extra_price(extra_id, price)


def update_visits():
    """
    With this function the discount for particular number of visits
    can be changed in the database.
    """
    visits = database_hotel.get_all_visits_discounts()
    visits_table = PrettyTable(["ID",
                                "From visit",
                                "To visit",
                                "Discount in %"])
    for visit in visits:
        visits_table.add_row(visit)
    print(visits_table)
    visit_id = input("Which discount do you want to alter?: ")
    visit_id = int(visit_id)
    discount = input("New discount in %: ")
    discount = int(discount)
    database_hotel.update_visits_discount(visit_id, discount)


def update_children():
    """
    With this function the discount for particular age of children
    can be changed in the database.
    """
    children = database_hotel.get_all_children_discounts()
    children_table = PrettyTable(["ID",
                                  "From age",
                                  "To age",
                                  "Discount in %"])
    for child in children:
        children_table.add_row(child)
    print(children_table)
    children_id = input("Which discount do you want to alter?: ")
    children_id = int(children_id)
    discount = input("New discount in %: ")
    discount = float(discount)
    database_hotel.update_children_discount(children_id, discount)
