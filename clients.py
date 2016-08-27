import database_hotel
from PIL import Image
import os
from prettytable import PrettyTable
import time
import smtplib
import getpass
import reservation_maker


clear = lambda: os.system('cls')


def menu(username):
    """
    This function serves as a menu for a logged in user
    @type username: string
    @param username: the username of the user
    """
    clear()
    client_info = database_hotel.get_client_info(username)
    name = client_info[0]
    print("Hello dear {}". format(name))
    while True:
        print("\nWhat would you like to do?\n")
        print("1. View our rooms")
        print("2. Look at our prices")
        print("3. Check out the discounts")
        print("4. Make a reservation")
        print("5. Cancel a resrvation")
        print("6. Check reservations")
        print("7. Pay a reservation")
        print("8. Check number of visits")
        print("9. Change password")
        print("10. Change bank account")
        print("11. Exit")
        choice = input("Option: ")
        choice = int(choice)
        if choice == 1:
            view_rooms()
        elif choice == 2:
            check_prices()
        elif choice == 3:
            check_discounts()
        elif choice == 4:
            make_a_reservation(username)
        elif choice == 5:
            cancel_a_reservation(username)
        elif choice == 6:
            check_reservations(username)
        elif choice == 7:
            pay_a_reservation(username)
        elif choice == 8:
            check_visits(username)
        elif choice == 9:
            change_a_password(username)
        elif choice == 10:
            change_bank(username)
        elif choice == 11:
            exit()
        else:
            print("Wrong input")


def make_a_reservation(username):
    """
    This function redirects to a different module.
    In which a reservation is added to the database
    @type username: string
    @param username: the username of the user 
    """
    reservation_maker.menu(username)


def view_rooms():
    """
    This function prints the different kind of rooms in the hotel. 
    """
    print("\nThe rooms we offer are the following:")
    print("Double rooms plus one child:")
    print("    * with view")
    print("    * with view + king-sized bed")
    print("    * AC")
    print("    * AC + king-sized bed")
    pic = input("Do you want to see a picture of this type of rooms(y/n)?: ")
    pic = str(pic)
    if pic == 'y':
        Image.open("flamingo_2_+_1.jpg").show()
    print("\nDouble rooms plus two children:")
    print("    * with view + AC")
    print("    * with view + AC + king-sized bed")
    print("    * no extras")
    print("    * king-sized bed")
    pic = input("Do you want to see a picture of this type of rooms(y/n)?: ")
    pic = str(pic)
    if pic == 'y':
        Image.open("flamingo_2_+_2.jpg").show()
    print("\nApartment of 2 adults plus 3 children:")
    print("    * with view + AC + king-sized bed + kitchen box")
    pic = input("Do you want to see a picture of this type of room(y/n)?: ")
    pic = str(pic)
    if pic == 'y':
        Image.open("flamingo_apartment.jpeg").show()
    print("\nWarning! Each extra is priced separately")


def check_prices():
    """
    This function prints the important information for a user
    from prices_rooms and prices_extra tables.
    """
    print("\n\nPrice per person!\n")
    rooms_table = PrettyTable(['Begin date',
                               'End date',
                               'Feeding type',
                               'Price'])
    rooms = database_hotel.get_all_room_prices()
    for period in rooms:
        rooms_table.add_row(period[1:])
    print(rooms_table)
    print("\n\nPrice for each extra!\n")
    extras_table = PrettyTable(['Extra',
                                'Price'])
    extras = database_hotel.get_all_extras()
    for extra in extras:
        extras_table.add_row(extra[1:])
    print(extras_table)


def check_discounts():
    """
    This function prints the important information for a user
    from visits_discount and children_discount tables.
    """
    print("\n\nDiscounts for loyal customers\n")
    visits_table = PrettyTable(['From visit',
                                'To visit',
                                'Discount in %'])
    visits = database_hotel.get_all_visits_discounts()
    for visit in visits:
        visits_table.add_row(visit[1:])
    print(visits_table)
    print("\n\nChildren discounts\n")
    children_table = PrettyTable(['From age',
                                  'To age',
                                  'Discount in %'])
    children = database_hotel.get_all_children_discounts()
    for child in children:
        children_table.add_row(child[1:])
    print(children_table)


def cancel_a_reservation(username):
    """
    This function removes a reservation made by a user of his choosing
    @type username: string
    @param username: the username of the user 
    """
    name = database_hotel.get_client_info(username)[0]
    email = database_hotel.get_client_email(username)
    print("\n\nYour reservation number was sent to you via email!")
    reservation_id = input("What is the number?: ")
    reservation_id = int(reservation_id)
    if not database_hotel.check_reservation_to_user(username, reservation_id):
        print("This reservation is not to your name!")
        time.sleep(2)
        clear()
        return
    text_full = """Hello, {},\n
                Your reservation(#{}) has been successfully cancelled.\n
                Full refund will be given to you.\n
                Have a good day! :)""".format(name, reservation_id)
    text_half = """Hello, {},\n
                Your reservation(#{}) has been successfully cancelled.\n
                Half refund will be given to you.\n
                Have a good day! :)""".format(name, reservation_id)
    if database_hotel.week_to_reservation(reservation_id):
        if database_hotel.check_if_payed(reservation_id):
            print("You have already paid for this reservation!")
            choice = input("Are you sure you want to cancel it?(y/n): ")
            if choice != 'y':
                return
        print("\nYour reservation has been cancelled.")
        print("A full refund will be given to you.")
        send_email(email, text_full)
    else:
        if database_hotel.check_if_payed(reservation_id):
            print("You have already paid for this reservation!")
            choice = input("Are you sure you want to cancel it?(y/n): ")
            if choice != 'y':
                return
        print("\nThere is less than a week to your reservation.")
        print("Only half of your money will be refunded")
        decide = input("Still sure?(y/n): ")
        if decide != 'y':
            return
        send_email(email, text_half)
    database_hotel.delete_reservation(reservation_id)
    database_hotel.downsize_client_visits(username)


def check_reservations(username):
    """
    This function shows only the upcoming reservations
    for the current user
    @type username: string
    @param username: the username of the user 
    """
    id_client = database_hotel.get_client_id(username)
    print("\n\nYour upcoming reservations are the following:")
    reservation_table = PrettyTable(['Begin date',
                                     'End date',
                                     'Adults',
                                     'Children',
                                     'Feeding type',
                                     'Extras',
                                     'Price',
                                     'Paid'])
    reservations = database_hotel.get_user_reservations(id_client)
    for reservation in reservations:
        reservation_table.add_row(reservation)
    print(reservation_table)


def send_email(user_mail, text):
    """
    This function sends an email to a given user's mail
    @type user_mail: string
    @param user_mail: the user's mail
    @type text: string
    @param text: the text message that will be sent
    """
    port = 587
    smtp_mail = 'smtp.gmail.com'
    system_mail = 'project.mail.fmi@gmail.com'
    system_pass = 'fmirules'
    server = smtplib.SMTP(smtp_mail, port)
    server.ehlo()
    server.starttls()
    server.login(system_mail, system_pass)
    server.sendmail(system_mail, user_mail, text)


def pay_a_reservation(username):
    """
    This function pays the reservation of an user.
    Sends email after the payment is done.
    @type username: string
    @param username: the username of the user 
    """
    print("\n\nYour reservation number was sent to you via email!")
    reservation_id = input("What is the number?: ")
    reservation_id = int(reservation_id)
    if not database_hotel.check_reservation_to_user(username, reservation_id):
        print("This reservation is not to your name!")
        time.sleep(2)
        return
    if database_hotel.check_if_payed(reservation_id):
        print("You have already paid for this reservation!")
        return
    database_hotel.pay_reservation(reservation_id)
    clear()
    print("Connecting to visa . . .")
    time.sleep(1)
    clear()
    print("Connecting to visa  . . .")
    time.sleep(1)
    clear()
    print("Connecting to visa . . .")
    time.sleep(1)
    clear()
    print("Connecting to visa  . . .")
    time.sleep(1)
    clear()
    print("Connecting to visa . . .")
    time.sleep(1)
    print("\nReady!!!\n")
    print("A confirmation email will be sent to you!")
    name = database_hotel.get_client_info(username)[0]
    text = """Hello, {},\n
           Your reservation(#{}) has been successfully paid.\n
    Have a good day :)""".format(name, reservation_id)
    user_mail = database_hotel.get_client_email(username)
    send_email(user_mail, text)


def check_visits(username):
    """
    This function checks the number of visits from the user so far.
    @type username: string
    @param username: the username of the user 
    """
    visits = database_hotel.get_client_visits(username)
    discount = database_hotel.get_visits_discount(visits)
    print("\nYour visits so far are {}. Which means you have {}% discount!\n"
          .format(visits, discount))


def change_a_password(username):
    """
    This function changes the password of a user in the database.
    @type username: string
    @param username: the username of the user 
    """
    old_pass = getpass.getpass(prompt="Old password: ")
    count = 1
    while not database_hotel.check_password(username, old_pass) and count != 3:
        print("Wrong password! Try again.")
        old_pass = getpass.getpass(prompt="Old password: ")
        count += 1
    if not database_hotel.check_password(username, old_pass):
        quit()
    new_pass = getpass.getpass(prompt="New password: ")
    confirm_pass = getpass.getpass(prompt="Confirm password: ")
    while new_pass != confirm_pass:
        print("Wrong confirmation password! Try again.")
        new_pass = getpass.getpass(prompt="New password: ")
        confirm_pass = getpass.getpass(prompt="Confirm password: ")
    database_hotel.change_password(username, new_pass)
    print("An email with your new password will be send to you")
    user_mail = database_hotel.get_client_email(username)
    text = """Hello,\n
           You just changed your password!\n
           Your new password is '{}'\n
           Have a nice day! :)""".format(new_pass)
    send_email(user_mail, text)
    clear()


def change_bank(username):
    """
    This function changes the bank information
    for the user in the database.
    @type username: string
    @param username: the username of the user 
    """
    bank_account = database_hotel.get_user_bank_info(username)
    print("\nYour current bank information is as follows: ")
    print("Card number: {}".format(bank_account[0]))
    print("Security number: {}".format(bank_account[1]))
    print("Experation month and year: {}".format(bank_account[2]))
    choice = input("Do you still want to change it?(y/n): ")
    if choice != 'y':
        return
    new_number = input("Your new card number: ")
    new_security = input("Your new security number: ")
    new_exp = input("Your new experation month and year(MM-YY): ")
    database_hotel.change_bank_account(
                                       username,
                                       new_number,
                                       new_security,
                                       new_exp)
    print("\nAll done!")
