import datetime

def get_date_from_weekday(base_date, weekday, time):
    """Gets the date from the weekday"""
    return base_date + datetime.timedelta(days=base_date.weekday() - weekday)