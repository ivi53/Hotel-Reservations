from database_hotel import *


def main():
    """
    This function runs when the file is opened.
    It creates the database and adds some information.
    """
    create()
    initialize_rooms()
    initialize_prices_rooms()
    initialize_prices_extras()
    initialize_visits_discount()
    initialize_children_discount()
    initialize_administrators()
    initialize_clients()
    initialize_reservations()


def initialize_rooms():
    """
    This function adds rooms to the rooms table in the database
    """
    for i in range(1, 5):
        add_room(i*100 + 1, 2, 3, "AC, View, King-sized bed, Kitchen box")
        add_room(i*100 + 2, 2, 1, "AC")
        add_room(i*100 + 3, 2, 1, "View")
        add_room(i*100 + 4, 2, 2, "")
        add_room(i*100 + 5, 2, 2, "View, AC")
        add_room(i*100 + 6, 2, 1, "AC, King-sized bed")
        add_room(i*100 + 7, 2, 1, "View, King-sized bed")
        add_room(i*100 + 8, 2, 2, "")
        add_room(i*100 + 9, 2, 2, "View, AC")
        add_room(i*100 + 10, 2, 1, "AC")
        add_room(i*100 + 11, 2, 1, "View")
        add_room(i*100 + 12, 2, 2, "King-sized bed")
        add_room(i*100 + 13, 2, 2, "View, King-sized bed, AC")
        add_room(i*100 + 14, 2, 1, "AC")
        add_room(i*100 + 15, 2, 1, "View")
        add_room(i*100 + 16, 2, 2, "")
        add_room(i*100 + 17, 2, 2, "View, AC")
        add_room(i*100 + 18, 2, 1, "AC, King-sized bed")
        add_room(i*100 + 19, 2, 1, "View, King-sized bed")
        add_room(i*100 + 20, 2, 2, "")
        add_room(i*100 + 21, 2, 2, "View, AC")
        add_room(i*100 + 22, 2, 1, "AC")
        add_room(i*100 + 23, 2, 1, "View")
        add_room(i*100 + 24, 2, 2, "King-sized bed")
        add_room(i*100 + 25, 2, 2, "View, King-sized bed, AC")
    conn.commit()


def initialize_prices_rooms():
    """
    This function adds periods with prices
    to the prices_rooms table in the database.
    """
    add_room_price("2016-6-01", "2016-6-19", "BB", 30)
    add_room_price("2016-6-01", "2016-6-19", "HB", 45)
    add_room_price("2016-6-01", "2016-6-19", "FB", 55)
    add_room_price("2016-6-20", "2016-7-18", "BB", 40)
    add_room_price("2016-6-20", "2016-7-18", "HB", 55)
    add_room_price("2016-6-20", "2016-7-18", "FB", 65)
    add_room_price("2016-7-19", "2016-8-31", "BB", 50)
    add_room_price("2016-7-19", "2016-8-31", "HB", 65)
    add_room_price("2016-7-19", "2016-8-31", "FB", 75)
    add_room_price("2016-9-01", "2016-9-14", "BB", 40)
    add_room_price("2016-9-01", "2016-9-14", "HB", 55)
    add_room_price("2016-9-01", "2016-9-14", "FB", 65)
    add_room_price("2016-9-15", "", "BB", 30)
    add_room_price("2016-9-15", "", "HB", 45)
    add_room_price("2016-9-15", "", "FB", 55)
    conn.commit()


def initialize_administrators():
    """
    This function adds administrators
    to the administrators table in the database
    """
    add_administrator("theAdmin", "imthebestadmin",
                      "Violeta Champoeva", "database admin")
    add_administrator("receptionist1", "weloveourjobhere",
                      "Kamelia Ivanova", "receptionist")
    add_administrator("receptionist2", "weloveourjobhere",
                      "Georgi Petrov", "receptionist")
    add_administrator("receptionist3", "weloveourjobhere",
                      "Maria Hristova", "receptionist")
    add_administrator("theBoss", "imthebestboss",
                      "Nikola Champoev", "manager")
    conn.commit()


def initialize_clients():
    """
    This function adds clients
    to the clients table in the database
    """
    add_client("ivi53", "12345678", "ivi53@abv.bg", "Iveta Champoeva",
               "Sofia", "951215****", 0, "1234567890", "1234", "2-2020")
    add_client("nas95", "12312345", "nas95@abv.bg", "Atanas Pavlov",
               "Sofia", "950516****", 0, "1234567890", "1234", "2-2020")
    add_client("villi", "321321", "ivi5317@gmail.com", "Violeta Champoeva",
               "Ruse", "720125****", 0, "1234567890", "1234", "2-2020")
    add_client("champo", "12345654", "nasr3052m@gmail.com", "Nikola Champoev",
               "Ruse", "700831****", 0, "1234567890", "1234", "2-2020")


def initialize_prices_extras():
    """
    This function adds extras with their price
    to the prices_extras table in the database
    """
    add_extra_price("King-sized bed", 5)
    add_extra_price("AC", 10)
    add_extra_price("View", 5)
    add_extra_price("Kitchen box", 10)
    add_extra_price("Mini bar", 5)
    conn.commit()


def initialize_visits_discount():
    """
    This function adds discounts for visits
    to the visits_discount table in the database
    """
    add_visit_discount(1, 2, 5)
    add_visit_discount(3, 4, 10)
    add_visit_discount(5, 6, 15)
    add_visit_discount(7, 8, 20)
    add_visit_discount(9, float("inf"), 25)
    conn.commit()


def initialize_children_discount():
    """
    This function adds discounts for children
    to the children_discount table in the database
    """
    add_children_discount(0, 2, 100)
    add_children_discount(3, 11, 70)
    add_children_discount(12, 18, 20)
    conn.commit()


def initialize_reservations():
    """
    This function adds reservations to the reservations table in the database
    """
    add_reservation(1, '2016-7-20', '2016-7-25', 2, 0, 'BB', "", 0, 203)
    add_reservation(1, '2016-8-01', '2016-8-05', 2, 0, 'BB', "", 0, 205)

if __name__ == '__main__':
    main()
