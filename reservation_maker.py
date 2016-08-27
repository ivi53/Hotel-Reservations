import database_hotel
import time
from date_type import *
import os
from prettytable import PrettyTable
import clients


clear = lambda: os.system('cls')


def menu(username):
    """
    This function is what makes the actual reservations.
    It searches for free rooms during a given period,
    calculates every added extra and every discount.
    @type username: string
    @param username: the username of the user
    """
    print("\nChoose carefully!")
    print("Keep in mind that the reservations are for the current year only!")
    print("When do you want your vacation to start?")
    begin_month = input("Month: ")
    begin_month = int(begin_month)
    begin_day = input("Day: ")
    begin_day = form_a_day(begin_day)
    print("\nWhen do you want your vacation to end?")
    end_month = input("Month: ")
    end_month = int(end_month)
    end_day = input("Day: ")
    end_day = form_a_day(end_day)
    today_year = database_hotel.today_define()[0:4]
    begin_date = "{}-{}-{}".format(today_year, begin_month, begin_day)
    end_date = "{}-{}-{}".format(today_year, end_month, end_day)
    if begin_date >= end_date:
        print("Wrong input. End date can't be earlier than the begin date!")
        time.sleep(2)
        clear()
        menu(username)
    if not date_validate(begin_month, begin_day) or\
       not date_validate(end_month, end_day):
        print("Wrong input. Try again!")
        time.sleep(2)
        clear()
        menu(username)
    num_primary = input("How many adults: ")
    num_primary = int(num_primary)
    num_extra = input("How many kids: ")
    num_extra = int(num_extra)
    if num_extra:
        first, second, third, fourth = age_define(num_extra)
    total_people = num_primary + num_extra
    if total_people <= 3:
        rooms = find_for_three(begin_date, end_date)
    elif total_people == 4:
        rooms = find_for_four(begin_date, end_date)
    elif total_people == 5:
        rooms = find_for_five(begin_date, end_date)
    else:
        print("We can't fit that many people in one room.")
        print("Try again.")
        time.sleep(2)
        clear()
        menu(username)
    if not rooms:
        print("Looks like we are all out of rooms! :(")
        time.sleep(2)
        return
    available_extras =\
        list(set([database_hotel.get_room_extras(room) for room in rooms]))
    available = PrettyTable(["Option",
                             "Extras"])
    count = 0
    for extra in available_extras:
        count += 1
        available.add_row((count, extra))
    print(available)
    print("\nChoose an option")
    option = input("Option: ")
    option = int(option)
    while option > len(available_extras) or option < 1:
        print("Wrong option! Try again.")
        print("\nChoose an option")
        option = input("Option: ")
        option = int(option)
    for room in rooms:
        if database_hotel.get_room_extras(room) == available_extras[option-1]:
            reserved_room = room
            break
    extras = available_extras[option-1].split(sep=', ')
    print("\nHow do you want to be fed?\n")
    while True:
        print("1. BB")
        print("2. HB")
        print("3. FB")
        feed = input("Option: ")
        feed = int(feed)
        if feed == 1:
            feed = 'BB'
            break
        elif feed == 2:
            feed = 'HB'
            break
        elif feed == 3:
            feed = 'FB'
            break
        else:
            print("Wrong input")
    price_person = database_hotel.get_price_per_person(begin_date,
                                                       end_date, feed)
    if num_extra:
        first_price = price_person -\
            price_person*database_hotel.get_children_discount(first)/100.0
        second_price = price_person -\
            price_person*database_hotel.get_children_discount(second)/100.0
        third_price = price_person -\
            price_person*database_hotel.get_children_discount(third)/100.0
        fourth_price = price_person -\
            price_person*database_hotel.get_children_discount(fourth)/100.0
    extras_price =\
        sum([database_hotel.get_extra_price(extra) for extra in extras])
    bar = input("Do you want a mini bar? It is priced seperately!(y/n): ")
    if bar == 'y':
        extras_price += database_hotel.get_extra_price("Mini bar")
    if num_extra:
        children_price =\
            child_pricing(num_extra, first_price, second_price,
                          third_price, fourth_price)
    else:
        children_price = 0
    price = num_primary*price_person + children_price + extras_price
    visits = database_hotel.get_client_visits(username)
    final_price = price -\
        price*database_hotel.get_visits_discount(visits)/100.0
    print("\nYour final price for the reservation is {}".format(final_price))
    choice = input("Do you still want to make it?(y/n): ")
    if choice != 'y':
        exit()
    if database_hotel.client_or_admin_login(username) == 'client':
        id_client = database_hotel.get_client_id(username)
        database_hotel.add_reservation(id_client, begin_date, end_date,
                                       num_primary, num_extra, feed,
                                       available_extras[option-1],
                                       final_price, reserved_room)
        database_hotel.update_client_visits(username)
        res_id = database_hotel.get_reservation_id(id_client, reserved_room)
        email = database_hotel.get_client_email(username)
        text = """Hello,\n
               You just made a reservation in our hotel.\n
               It's identification number is {}\n
               It's price is {}\n
               You have to pay it in full one week before the reservation\n
               """.format(res_id, final_price)
        clients.send_email(email, text)
    else:
        id_admin = database_hotel.get_admin_id(username)
        res_id = database_hotel.get_reservation_id(id_admin, reserved_room)
        database_hotel.add_reservation(id_admin, begin_date, end_date,
                                       num_primary, num_extra, feed,
                                       available_extras[option-1],
                                       final_price, reserved_room)
        database_hotel.pay_reservation(res_id)


def find_for_three(begin, end_):
    """
    This function seraches for rooms fit for 3 or less people.
    It returns a list of the available room numbers
    @type begin: string
    @param begin: the begining of the searched period
    @type end_: string
    @param end_: the ending of the searched period
    @rtype: list
    @return: a list of available room numbers
    """
    triple_rooms = database_hotel.get_triple_rooms()
    occupied = set(database_hotel.get_occupied_smallest_rooms(begin, end_))
    for num in occupied:
        if num in triple_rooms:
            triple_rooms.remove(num)
    if not triple_rooms:
        return find_for_four(begin, end_)
    return triple_rooms


def find_for_four(begin, end_):
    """
    This function seraches for rooms fit for 4 people.
    It returns a list of the available room numbers
    @type begin: string
    @param begin: the begining of the searched period
    @type end_: string
    @param end_: the ending of the searched period
    @rtype: list
    @return: a list of available room numbers
    """
    quadruple_rooms = database_hotel.get_quadruple_rooms()
    occupied = set(database_hotel.get_occupied_bigger_rooms(begin, end_, 4))
    for num in occupied:
        if num in quadruple_rooms:
            quadruple_rooms.remove(num)
    if not quadruple_rooms:
        return find_for_five(begin, end_)
    return quadruple_rooms


def find_for_five(begin, end_):
    """
    This function seraches for rooms fit for 5 people.
    It returns a list of the available room numbers
    @type begin: string
    @param begin: the begining of the searched period
    @type end_: string
    @param end_: the ending of the searched period
    @rtype: list
    @return: a list of available room numbers
    """
    apartment_rooms = database_hotel.get_apartment_rooms()
    occupied = set(database_hotel.get_occupied_bigger_rooms(begin, end_, 5))
    for num in occupied:
        if num in apartment_rooms:
            apartment_rooms.remove(num)
    if not apartment_rooms:
        return []
    return apartment_rooms


def child_pricing(num, first, second, third, fourth):
    """
    This function helps me calculate the children price
    for the reservation.
    @type num: integer
    @param num: the number of kids
    @type first: float
    @param first: the price for the first child
    @type second: float
    @param second: the price for the second child
    @type third: float
    @param third: the price for the third child
    @type fourth: float
    @param fourth: the price for the fourth child
    """
    if num == 1:
        return first
    if num == 2:
        return first + second
    if num == 3:
        return first + second + third
    if num == 4:
        return first + second + third + fourth


def age_define(num):
    """
    This function fills the age for each children.
    Even if it isn't needed.
    @type num: integer
    @param num: the number kids attending
    @rtype: tuple
    @return: returns the years of the children
    """
    if num == 1:
        first = input("How old is the first child?: ")
        first = int(first)
        second = 20
        third = 20
        fourth = 20
    elif num == 2:
        first = input("How old is the first child?: ")
        first = int(first)
        second = input("How old is the second child?: ")
        second = int(second)
        third = 20
        fourth = 20
    elif num == 3:
        first = input("How old is the first child?: ")
        first = int(first)
        second = input("How old is the second child?: ")
        second = int(second)
        third = input("How old is the third child?: ")
        third = int(third)
        fourth = 20
    else:
        first = input("How old is the first child?: ")
        first = int(first)
        second = input("How old is the second child?: ")
        second = int(second)
        third = input("How old is the third child?: ")
        third = int(third)
        fourth = input("How old is the fourth child?: ")
        fourth = int(fourth)
    return first, second, third, fourth


def form_a_day(day):
    """
    Makes a one-digit number into a one-digit number
    with a '0' in front
    @type day: string
    @param day: some number to be converted
    @rtype: string
    @return: returns the converted number in str type
    """
    day = int(day)
    if day in range(1, 10):
        day = '0' + str(day)
    return day
