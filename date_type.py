days_per_month = {
    '1': 31,
    '2': 28,
    '3': 31,
    '4': 30,
    '5': 31,
    '6': 30,
    '7': 31,
    '8': 31,
    '9': 30,
    '10': 31,
    '11': 30,
    '12': 31
}


def date_validate(month, day):
    """
    This function makes sure that the date is valid
    according to the month and days in combination
    @type month: integer or string
    @param month: the month we want to check
    @type day: integer or string
    @param day: the day we want to check
    @rtype: bool
    @return: true if it is a valid date, false otherwise
    """
    day = int(day)
    month = int(month)
    if str(month) not in days_per_month.keys():
        return False
    if day > days_per_month[str(month)] or day < 1:
        return False
    return True


def date_extend(month, year):
    """
    A function to help me not write the same thing many times.
    If the month is December the month switches to January next year
    @type month: integer
    @param month: a month of the year
    @type day: integer
    @param day: a day of the given month
    @rtype: tuple
    @return: returns the new month and year
    """
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    return (month, year)


class Date_YY_MM_DD:
    """
    A helpful class that lets me easily calculate periods
    from date to date when the dates themselves are represented as strings
    """
    def __init__(self, str_date):
        self.original = str_date
        date = str_date.split(sep='-')
        self.year = int(date[0])
        self.month = int(date[1])
        self.days = int(date[2])

    def get_days(self):
        return self.days

    def get_month(self):
        return self.month

    def get_year(self):
        return self.year

    def __str__(self):
        return self.original

    def __sub__(self, other):
        """
        Calculates how many days are between the two dates.
        """
        year_dif = other.get_year() - self.year
        month_dif = other.get_month() - self.month
        day_dif = other.get_days() - self.days
        days = 0
        if not year_dif:
            if not month_dif:
                if not day_dif:
                    return 0
                else:
                    days += day_dif
            else:
                days = other.get_days()
                for key in range(other.get_month()-1, self.month, -1):
                    days += days_per_month[str(key)]
                days += days_per_month[str(self.month)] - self.days
        else:
            days += year_dif*365
            temp_date = Date_YY_MM_DD('{}-{}-{}'.format(self.year+1,
                                                        self.month, self.days))
            days -= (other - temp_date)
        return days

    def __add__(self, days):
        """
        Calculates the new date after all the given days are added.
        """
        end_year = self.year
        end_month = self.month
        end_days = self.days
        if end_days + days <= days_per_month[str(end_month)]:
            end_days += days
        else:
            days -= (days_per_month[str(end_month)] - end_days) + 1
            end_days = 1
            end_month, end_year = date_extend(end_month, end_year)
            while days > days_per_month[str(end_month)] - 1:
                days -= days_per_month[str(end_month)]
                end_month, end_year = date_extend(end_month, end_year)
            end_days += days
        final = '{}-{}-{}'.format(end_year, end_month, end_days)
        return Date_YY_MM_DD(final)
