import sqlite3
from date_type import *
import datetime

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()


def create():
    """
    This function creates all the tables of the database.
    """
    create_rooms()
    create_clients()
    create_reservations()
    create_administrators()
    create_prices_rooms()
    create_prices_extras()
    create_visits_discount()
    create_children_discount()


def create_rooms():
    """
    Creats rooms table
    """
    query = """CREATE TABLE IF NOT EXISTS
            rooms(number INTEGER PRIMARY KEY,
                  floor INTEGER NOT NULL,
                  num_primary INTEGER NOT NULL,
                  num_extra INTEGER,
                  extras TEXT)"""
    cursor.execute(query)


def create_clients():
    """
    Creates clients table
    """
    query = """CREATE TABLE IF NOT EXISTS
            clients(id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    email TEXT UNIQUE,
                    first_last_name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    ucn TEXT NOT NULL,
                    visits INTEGER,
                    card_number TEXT,
                    security_number TEXT,
                    month_year TEXT)"""
    cursor.execute(query)


def create_reservations():
    """
    Creates reservations table
    """
    query = """CREATE TABLE IF NOT EXISTS
            reservations(id INTEGER PRIMARY KEY AUTOINCREMENT,
                         id_client INTEGER,
                         begin_date DATE NOT NULL,
                         end_date DATE NOT NULL,
                         num_primary INTEGER NOT NULL,
                         num_extra INTEGER NOT NULL,
                         feed_type TEXT NOT NULL,
                         extras TEXT,
                         price REAL NOT NULL,
                         problems TEXT,
                         problems_price REAL,
                         paid INTEGER,
                         room INTEGER)"""
    cursor.execute(query)


def create_administrators():
    """
    Creates administrators table
    """
    query = """CREATE TABLE IF NOT EXISTS
            administrators(id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT UNIQUE,
                           password TEXT NOT NULL,
                           first_last_name TEXT,
                           job TEXT NOT NULL)"""
    cursor.execute(query)


def create_prices_rooms():
    """
    Creates prices_rooms table
    """
    query = """CREATE TABLE IF NOT EXISTS
            prices_rooms(id INTEGER PRIMARY KEY AUTOINCREMENT,
                         begin_date DATE NOT NULL,
                         end_date DATE NOT NULL,
                         feed_type TEXT NOT NULL,
                         price REAL NOT NULL)"""
    cursor.execute(query)


def create_prices_extras():
    """
    Creates prices_extras table
    """
    query = """CREATE TABLE IF NOT EXISTS
            prices_extras(id INTEGER PRIMARY KEY AUTOINCREMENT,
                          extra TEXT UNIQUE,
                          price REAL NOT NULL)"""
    cursor.execute(query)


def create_visits_discount():
    """
    Creates visits_discount table
    """
    query = """CREATE TABLE IF NOT EXISTS
            visits_discount(id INTEGER PRIMARY KEY AUTOINCREMENT,
                            from_visits INTEGER UNIQUE,
                            to_visits INTEGER UNIQUE,
                            discount INTEGER NOT NULL)"""
    cursor.execute(query)


def create_children_discount():
    """
    Creates children_discount table
    """
    query = """CREATE TABLE IF NOT EXISTS
            children_discount(id INTEGER PRIMARY KEY AUTOINCREMENT,
                              from_age INTEGER UNIQUE,
                              to_age INTEGER UNIQUE,
                              discount INTEGER NOT NULL)"""
    cursor.execute(query)


def add_room(number_room, num_primary, num_extra, extras):
    """
    Adds a room in the rooms table
    @type number_room: integer
    @param number_room: the number of the new room
    @type num_primary: integer
    @param num_primary: the number of adults for the new room
    @type num_extra: integer
    @param num_extra: the number of children for the new room
    @type extras: string
    @param extras: the extras that go along with the new room
    """
    query = """INSERT INTO rooms
            (number, floor, num_primary, num_extra, extras)
            VALUES(?, ?, ?, ?, ?)"""
    cursor.execute(query,
                   (number_room, (int)(number_room/100),
                    num_primary, num_extra,
                    extras))


def delete_room(number_room):
    """
    This function deletes a record in rooms table
    @type number_room: integer
    @param number_room: the number of the room to be removed
    """
    query = """DELETE FROM rooms
            WHERE number=?"""
    cursor.execute(query, (number_room, ))
    conn.commit()


def get_room_extras(number_room):
    """
    This function return the extras of a given room
    @type number_room: integer
    @param number_room: the number of the room
    @rtype: string
    @return: the extras of a given room
    """
    query = """SELECT extras FROM rooms
            WHERE number=?"""
    cursor.execute(query, (number_room, ))
    extra = cursor.fetchone()
    if not extra:
        return 'Normal'
    return extra[0]


def get_all_rooms():
    """
    This function returns all the rooms from rooms table
    @rtype: tuple
    @return: all the rooms in rooms table
    """
    query = """SELECT number, floor, num_primary, num_extra, extras
            FROM rooms"""
    cursor.execute(query)
    return cursor.fetchall()


def get_different_kind_rooms(children):
    """
    This function returns a list of different room numbers
    based on the number of people in the room.
    @type children: integer
    @param children: the number of extra people
    @rtype: list
    @return a list of room numbers
    """
    query = """SELECT number FROM rooms
            WHERE num_extra=?"""
    cursor.execute(query, (children, ))
    rooms = cursor.fetchall()
    return [num for room in rooms for num in room]


def get_triple_rooms():
    """
    This function return a list of all triple rooms
    @rtype: list
    @return: a list of every triple room number
    """
    return get_different_kind_rooms(1)


def get_quadruple_rooms():
    """
    This function return a list of all quadruple rooms
    @rtype: list
    @return: a list of every quadruple room number
    """
    return get_different_kind_rooms(2)


def get_apartment_rooms():
    """
    This function return a list of all apartment rooms
    @rtype: list
    @return: a list of every apartment room number
    """
    return get_different_kind_rooms(3)


def add_client(username, password, email, name, address,
               ucn, visits, card_num, security_num, card_month_year):
    """
    Adds a client in the clients table
    @type username: string
    @param username: the username of the client
    @type password: string
    @param password: chosen password from the client
    @type email: string
    @param email: the email provided from the client
    @type name: string
    @param name: the name provided from the client
    @type address: string
    @param address: the address of the client, can be ommited
    @type ucn: string
    @param ucn: the ucn of the client
    @type visits: integer
    @param visits: the number of visits to the hotel from this user
    @type card_num: string
    @param card_num: the card number of the user
    @type security_num: string
    @param security_num: the sucurity number of the client's card
    @type card_month_year: string
    @param card_month_year: the experation date of the client's card
    """
    query = """INSERT INTO clients
            (username, password, email, first_last_name, address, ucn,
            visits, card_number, security_number, month_year)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (username, hash_password(password),
                           email, name, address, ucn, visits,
                           card_num, security_num, card_month_year))
    conn.commit()


def delete_client(username):
    """
    This function deletes a client from clients table
    @type username: string
    @param username: the username of the user
    """
    query = """DELETE FROM clients
            WHERE username=?"""
    cursor.execute(query, (username, ))
    conn.commit()


def get_client_email(username):
    """
    This function returns the email of a given client by email
    @type username: string
    @param username: the username of the user
    @rtype: string
    @return: returns the email of the wanted user
    """
    query = """SELECT email FROM clients
            WHERE username=?"""
    cursor.execute(query, (username, ))
    return cursor.fetchone()[0]


def get_client_visits(username):
    """
    This function returns the visits made by a client
    @type username: string
    @param username: the username of the user
    @rtype: integer
    @return: returns the number of visits of the wanted user
    """
    query = """SELECT visits FROM clients
            WHERE username=?"""
    cursor.execute(query, (username, ))
    visits = cursor.fetchone()
    if not visits:
        return 0
    return visits[0]


def get_client_id(username):
    """
    This function returns the ID of a given client
    @type username: string
    @param username: the username of the user
    @rtype: integer
    @return: returns the ID of the wanted user
    """
    query = """SELECT id FROM clients
            WHERE username=?"""
    cursor.execute(query, (username, ))
    return cursor.fetchone()[0]


def downsize_client_visits(username):
    """
    This function reduces the visits of a given client by one
    @type username: string
    @param username: the username of the user
    """
    visits = get_client_visits(username) - 1
    query = """UPDATE clients SET visits=?
            WHERE username=?"""
    cursor.execute(query, (visits, username))
    conn.commit()


def update_client_visits(username, *args):
    """
    This function increase the visits of a given client
    by one or more
    @type username: string
    @param username: the username of the user
    @type *args: integer
    @param *args: visits can be set a wanted value
    """
    if not args:
        visits = get_client_visits(username) + 1
    else:
        visits = args[0]
    query = """UPDATE clients SET visits=?
            WHERE username=?"""
    cursor.execute(query, (visits, username))
    conn.commit()


def is_username_free(username):
    """
    This function checks whether an username is free or not
    @type username: string
    @param username: the username of the user
    @rtype: bool
    @return: returns true if the username is free, false otherwise
    """
    query = """SELECT username FROM clients
            WHERE username=?"""
    cursor.execute(query, (username, ))
    if not cursor.fetchone():
        return True
    return False


def check_password(username, password):
    """
    This function checks whether a password is correct
    for the given username
    @type username: string
    @param username: the username of the user
    @type password: string
    @param password: the password that we want to check
    @rtype: bool
    @return: true if the password matches, false otherwise
    """
    query = """SELECT password FROM clients
            WHERE username=?"""
    cursor.execute(query, (username, ))
    actual_pass = cursor.fetchone()
    if not actual_pass:
        return False
    if actual_pass[0] == hash_password(password):
        return True
    return False


def get_client_info(username):
    """
    This function returns information about a given user
    @type username: string
    @param username: the username of the user
    @rtype: tuple
    @return: returns a tuple with information about the client
    """
    query = """SELECT first_last_name, address, ucn FROM clients
            WHERE username=?"""
    cursor.execute(query, (username, ))
    return cursor.fetchone()


def get_user_bank_info(username):
    """
    This function returns bank information about a given user
    @type username: string
    @param username: the username of the user
    @rtype: tuple
    @return: returns a tuple with bank information about the client
    """
    query = """SELECT card_number, security_number, month_year
            FROM clients WHERE username=?"""
    cursor.execute(query, (username, ))
    return cursor.fetchone()


def change_password(username, new_pass):
    """
    This function changes the password of a user
    with a different one
    @type username: string
    @param username: the username of the user
    @type new_pass: string
    @param new_pass: the newly chosen password
    """
    password = hash_password(new_pass)
    query = """UPDATE clients SET password=?
            WHERE username=?"""
    cursor.execute(query, (password, username))
    conn.commit()


def change_bank_account(username, card, security, exp):
    """
    This function changes the bank account of a user
    with a different one
    @type username: string
    @param username: the username of the user
    @type card: string
    @param card: the new card number
    @type security: string
    @param security: the new security number for the card
    @type exp: string
    @param exp: the new expiration date
    """
    query = """UPDATE clients SET card_number=?, security_number=?, month_year=?
            WHERE username=?"""
    cursor.execute(query, (card, security, exp, username))
    conn.commit()


def hash_password(password):
    """
    This function is for saving passwords in a discreet way
    @type password: string
    @param password: the password to be 'hashed'
    """
    hashed = ''
    for ch in password:
        hashed = hashed + str(ord(ch))
    return hashed[::-1]


def add_reservation(id_client, begin, end, primary,
                    extra_people, feed_type, extras, price, room):
    """
    Adds a reservation in the reservations table
    @type id_client: integer
    @param id_client: the ID of the client
    @type begin: integer
    @param begin: the begining of the reservation
    @type end: integer
    @param end: the ending of the reservation
    @type primary: integer
    @param primary: the number of adults
    @type extra_people: integer
    @param extra_people: the number of children
    @type feed_type: string
    @param feed_type: the type of feeding in the hotel
    @type extras: string
    @param extras: the extras added to the reservation
    @type price: float
    @param price: the total price of the reservation
    @type room: integer
    @param room: the number of the available room
    """
    query = """INSERT INTO reservations
            (id_client, begin_date, end_date, num_primary, num_extra,
            feed_type, extras, price, problems, problems_price, paid, room)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, (id_client, begin, end, primary, extra_people,
                           feed_type, extras, price, "none", 0, 0, room))
    conn.commit()


def delete_reservation(id_reservation):
    """
    This function is for deleting reservations
    from reservations table
    @type id_reservation: integer
    @param id_reservation: the ID of the wanted reservation
    """
    query = """DELETE FROM reservations
            WHERE id=?"""
    cursor.execute(query, (id_reservation, ))
    conn.commit()


def clear_old_reservations():
    """
    This function is for clearing old rercords
    in the reservations table 
    """
    today = str(datetime.datetime.today())[0:10]
    today_date = today.split(sep='-')
    last_year = str(int(today_date[0]) - 1)
    last_year_date = "{}-{}-{}".format(last_year, today_date[1], today_date[2])
    query = """DELETE FROM reservations
            WHERE end_date<=?"""
    cursor.execute(query, (last_year_date, ))
    conn.commit()


def pay_reservation(id_reservation):
    """
    This function is for paying a reservation
    @type id_reservation: integer
    @param id_reservation: the ID of the reservation
                           which someone wants to pay
    """
    query = """UPDATE reservations SET paid=1
            WHERE id=?"""
    cursor.execute(query, (id_reservation, ))
    conn.commit()


def add_problems(id_reservation, problems, problems_price):
    query = """UPDATE reservations SET problems=?, problems_price=?
            WHERE id=?"""
    cursor.execute(query, (problems, problems_price, id_reservation))
    conn.commit()


def get_user_reservations(id_client):
    today = today_define()
    query = """SELECT begin_date, end_date, num_primary, num_extra,
            feed_type, extras, price, paid
            FROM reservations WHERE id_client=? AND begin_date>=?"""
    cursor.execute(query, (id_client, today))
    return cursor.fetchall()


def get_reservation_problems(id_reservation):
    query = """SELECT problems, problems_price FROM reservations
            WHERE id=?"""
    cursor.execute(query, (id_reservation, ))
    return cursor.fetchone()


def check_if_payed(id_reservation):
    query = """SELECT price FROM reservations
            WHERE id=? AND paid=1"""
    cursor.execute(query, (id_reservation, ))
    if not cursor.fetchone():
        return False
    return True


def get_current_reservation_id_from_name(name, room):
    today = today_define()
    query = """SELECT id FROM reservations
            WHERE name=? AND room=? AND ? BETWEEN begin_date AND end_date"""
    cursor.execute(query, (name, room, today))
    return cursor.fetchone()[0]


def get_reservation_id(id_client, room):
    today = today_define()
    query = """SELECT id FROM reservations
            WHERE id_client=? AND room=? AND begin_date>=?"""
    cursor.execute(query, (id_client, room, today))
    id_res = cursor.fetchone()
    if not id_res:
        return 0
    return id_res[0]


def get_reservation_info(id_reservation):
    query = """SELECT begin_date, end_date, num_primary, num_extra,
            feed_type, extras, price, paid
            FROM reservations WHERE id=?"""
    cursor.execute(query, (id_reservation, ))
    return cursor.fetchone()


def get_all_reservations():
    query = """SELECT id, begin_date, end_date, num_primary, num_extra,
            feed_type, extras, price, paid FROM reservations"""
    cursor.execute(query)
    return cursor.fetchall()


def week_to_reservation(reservation_id):
    today = today_define()
    query = """SELECT begin_date FROM reservations
            WHERE id=?"""
    cursor.execute(query, (reservation_id, ))
    begin_date = cursor.fetchone()[0]
    if Date_YY_MM_DD(today) - Date_YY_MM_DD(begin_date) >= 7:
        return True
    return False


def check_reservation_to_user(username, reservation_id):
    query = """SELECT id_client FROM reservations
        WHERE id=?"""
    cursor.execute(query, (reservation_id, ))
    current = cursor.fetchone()
    id_client = get_client_id(username)
    if not current:
        return False
    if id_client == current[0]:
        return True
    return False


def get_occupied_smallest_rooms(begin_, end_):
    query = """SELECT room FROM reservations
            WHERE num_primary+num_extra<=3 AND
            (begin_date<=? AND end_date>?
            OR begin_date<? AND end_date>=?
            OR begin_date>=? AND end_date<=?)"""
    cursor.execute(query, (begin_, begin_, end_, end_, begin_, end_))
    rooms = cursor.fetchall()
    return [num for room in rooms for num in room]


def get_occupied_bigger_rooms(begin_, end_, total):
    query = """SELECT room FROM reservations
            WHERE num_primary+num_extra=? AND
            (begin_date<=? AND end_date>?
            OR begin_date<? AND end_date>=?)"""
    cursor.execute(query, (total, begin_, begin_, end_, end_))
    rooms = cursor.fetchall()
    return [num for room in rooms for num in room]


def add_administrator(username, password, name, job):
    """
    Adds an administrator in the administrators table
    @type username: string
    @param username: the username of the administrator
    @type password: string
    @param password: the password of the administrator
    @type name: string
    @param name: the name of the administrator
    @type job: string
    @param job: the position of the administrator
    """
    query = """INSERT INTO administrators
            (username, password, first_last_name, job)
            VALUES(?, ?, ?, ?)"""
    cursor.execute(query, (username, hash_password(password), name, job))


def delete_administrator(username):
    query = """DELETE FROM administrators
            WHERE username=?"""
    cursor.execute(query, (username, ))
    conn.commit()


def is_admin_free(username):
    query = """SELECT username FROM administrators
            WHERE username=?"""
    cursor.execute(query, (username, ))
    if not cursor.fetchone():
        return True
    return False


def admin_pass(username, password):
    query = """SELECT password FROM administrators
            WHERE username=?"""
    cursor.execute(query, (username, ))
    actual_pass = cursor.fetchone()
    if not actual_pass:
        return False
    if actual_pass[0] == hash_password(password):
        return True
    return False


def get_job(username):
    query = """SELECT job FROM administrators
            WHERE username=?"""
    cursor.execute(query, (username, ))
    return cursor.fetchone()[0]


def get_admin_id(username):
    query = """SELECT id FROM administrators
            WHERE username=?"""
    cursor.execute(query, (username, ))
    return cursor.fetchone()[0]


def get_admin_info(username):
    query = """SELECT first_last_name, job FROM administrators
            WHERE username=?"""
    cursor.execute(query, (username, ))
    return cursor.fetchone()


def add_room_price(begin, end_, type_, price):
    """
    Adds a period with price in the prices_rooms table
    @type begin: string
    @param begin: the begining of the period
    @type end_: string
    @param end_: the ending of the period
    @type type_: string
    @param type_: the type of feeding
    @type price: integer
    @param price: the price for the period with the feeding
    """
    query = """INSERT INTO prices_rooms
            (begin_date, end_date, feed_type, price)
            VALUES(?, ?, ?, ?)"""
    cursor.execute(query, (begin, end_, type_, price))


def delete_room_price(begin, end, type_):
    query = """DELETE FROM prices_rooms
            WHERE begin_date=? AND end_date=? AND feed_type=?"""
    cursor.execute(query, (begin, end, type_))
    conn.commit()


def get_all_room_prices():
    query = """SELECT id, begin_date, end_date, feed_type, price
            FROM prices_rooms"""
    cursor.execute(query)
    return cursor.fetchall()


def update_room_price(id_period, price):
    query = """UPDATE prices_rooms SET price=?
            WHERE id=?"""
    cursor.execute(query, (price, id_period))
    conn.commit()


def check_unique_room_price(begin, end, type_):
    query = """SELECT price FROM prices_rooms
            WHERE begin_date=? AND end_date=? AND feed_type=?"""
    cursor.execute(query, (begin, end, type_))
    if not cursor.fetchone()[0]:
        return True
    return False


def set_rooms_period_for_next_year():
    today = str(datetime.datetime.today())[0:10]
    today_date = today.split(sep='-')
    last_year = str(int(today_date[0]) - 1)
    last_year_date = "{}-{}-{}".format(last_year, today_date[1], today_date[2])
    query_get = """SELECT begin_date, end_date FROM prices_rooms"""
    cursor.execute(query_get)
    periods = cursor.fetchall()
    new_periods = [
        tuple([str(Date_YY_MM_DD(part) + 365) for part in period])
        for period in periods]
    query_update = """UPDATE prices_rooms SET begin_date=?, end_date=?
                   WHERE id=?"""
    id_room = 1
    for period in new_periods:
        cursor.execute(query_update, (period[0], period[1], id_room))
        id_room += 1
    conn.commit()


def getting_periods_helper(begin_, type_):
    query = """SELECT end_date, price FROM prices_rooms
            WHERE begin_date<=? AND end_date>=? AND feed_type=?"""
    cursor.execute(query, (begin_, begin_, type_))
    return cursor.fetchone()


def get_price_per_person(begin_, end_, type_):
    price = 0
    query_max_period = """SELECT MAX(begin_date)
                       FROM prices_rooms
                       WHERE feed_type=?"""
    cursor.execute(query_max_period, (type_, ))
    max_period = cursor.fetchone()[0]
    if begin_ >= max_period:
        query = """SELECT price FROM prices_rooms
                WHERE begin_date=? AND feed_type=?"""
        cursor.execute(query, (max_period, type_))
        period_price = cursor.fetchone()[0]
        price += (Date_YY_MM_DD(begin_) - Date_YY_MM_DD(end_))*period_price
        return price
    result = getting_periods_helper(begin_, type_)
    end_period = result[0]
    period_price = result[1]
    if end_ <= end_period:
        price += (Date_YY_MM_DD(begin_) - Date_YY_MM_DD(end_))*period_price
        return price
    while end_ > end_period:
        price += (Date_YY_MM_DD(begin_) - Date_YY_MM_DD(end_period) + 1)\
            * period_price
        begin_ = str(Date_YY_MM_DD(end_period) + 1)
        if begin_ == max_period:
            query = """SELECT price FROM prices_rooms
                    WHERE begin_date=? AND feed_type=?"""
            cursor.execute(query, (max_period, type_))
            period_price = cursor.fetchone()[0]
            price += (Date_YY_MM_DD(begin_) - Date_YY_MM_DD(end_))*period_price
            return price
        else:
            result = getting_periods_helper(begin_, type_)
            end_period = result[0]
            period_price = result[1]
    price += (Date_YY_MM_DD(begin_) - Date_YY_MM_DD(end_) + 1)*period_price
    return price


def add_extra_price(extra, price):
    """
    Adds an extra with price in the prices_extras table
    @type extra: string
    @param extra: the extra
    @type price: integer
    @param price: the price of the extra
    """
    query = """INSERT INTO prices_extras
            (extra, price)
            VALUES(?, ?)"""
    cursor.execute(query, (extra, price))


def delete_extra_price(id_extra):
    query = """DELETE FROM prices_extras
            WHERE id=?"""
    cursor.execute(query, (id_extra, ))
    conn.commit()


def update_extra_price(id_extra, price):
    query = """UPDATE prices_extras SET price=?
            WHERE id=?"""
    cursor.execute(query, (price, id_extra))
    conn.commit()


def get_all_extras():
    query = """SELECT id, extra, price FROM prices_extras"""
    cursor.execute(query)
    return cursor.fetchall()


def get_extra_price(extra):
    query = """SELECT price FROM prices_extras
            WHERE extra=?"""
    cursor.execute(query, (extra, ))
    return cursor.fetchone()[0]


def add_visit_discount(from_, to, discount):
    """
    Adds a discount for visits in the visits_discount table
    @type from_: integer
    @param from_: from how many visits
    @type to: integer
    @param to: to how many visits
    @type discount: integer
    @param discount: the discount for the given period
    """
    query = """INSERT INTO visits_discount
            (from_visits, to_visits, discount)
            VALUES(?, ?, ?)"""
    cursor.execute(query, (from_, to, discount))


def delete_visit_discount(id_discount):
    query = """DELETE FROM visits_discount
            WHERE id=?"""
    cursor.execute(query, (id_discount))
    conn.commit()


def update_visits_discount(id_discount, discount):
    query = """UPDATE visits_discount SET discount=?
            WHERE id=?"""
    cursor.execute(query, (discount, id_discount))
    conn.commit()


def get_all_visits_discounts():
    query = """SELECT id, from_visits, to_visits, discount
            FROM visits_discount"""
    cursor.execute(query)
    return cursor.fetchall()


def get_visits_discount(visits):
    if visits == 0:
        return 0
    query = """SELECT MAX(from_visits)
            FROM visits_discount"""
    cursor.execute(query)
    max_visits = cursor.fetchone()[0]
    if visits >= max_visits:
        query = """SELECT discount FROM visits_discount
                WHERE from_visits=?"""
        cursor.execute(query, (max_visits))
        return cursor.fetchone()[0]
    query = """SELECT discount FROM visits_discount
            WHERE ? BETWEEN from_visits AND to_visits"""
    cursor.execute(query, (visits, ))
    return cursor.fetchone()[0]


def add_children_discount(from_, to, discount):
    """
    Adds a discount for children age in the children_discount table
    @type from_: integer
    @param from_: from how many years
    @type to: integer
    @param to: to how many years
    @type discount: integer
    @param discount: the discount for the given period
    """
    query = """INSERT INTO children_discount
            (from_age, to_age, discount)
            VALUES(?, ?, ?)"""
    cursor.execute(query, (from_, to, discount))


def delete_visit_discount(id_discount):
    query = """DELETE FROM children_discount
            WHERE id=?"""
    cursor.execute(query, (id_discount))
    conn.commit()


def update_children_discount(id_discount, discount):
    query = """UPDATE children_discount SET discount=?
            WHERE id=?"""
    cursor.execute(query, (discount, id_discount))
    conn.commit()


def get_all_children_discounts():
    query = """SELECT id, from_age, to_age, discount
            FROM children_discount"""
    cursor.execute(query)
    return cursor.fetchall()


def get_children_discount(child):
    query = """SELECT MAX(to_age)
            FROM children_discount"""
    cursor.execute(query)
    max_age = cursor.fetchone()[0]
    if child >= max_age:
        return 0
    query = """SELECT discount FROM children_discount
            WHERE ? BETWEEN from_age AND to_age"""
    cursor.execute(query, (child, ))
    return cursor.fetchone()[0]


def client_or_admin_login(username):
    if not is_username_free(username):
        return 'client'
    if not is_admin_free(username):
        return 'admin'
    return 'not registered'


def today_define():
    today = str(datetime.datetime.today())[0:10]
    today_date = today.split(sep='-')
    today_year = today_date[0]
    today_month = str(int(today_date[1]))
    today_day = str(int(today_date[2]))
    return "{}-{}-{}".format(today_year, today_month, today_day)
