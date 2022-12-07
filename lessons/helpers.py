import datetime

def get_date_from_weekday(base_date, weekday, time):
    """Gets the date from the weekday"""
    today = datetime.date.today()
    today = datetime.datetime.combine(today, time)
    return today + datetime.timedelta(days=today.weekday() - weekday)