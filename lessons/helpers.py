import datetime
from lessons.models import Lesson

def get_date_from_weekday(weekday, time):
    """Gets the date from the weekday"""
    today = datetime.date.today()
    today = datetime.datetime.combine(today, time)
    return today + datetime.timedelta(days=today.weekday() - weekday)

def get_available_terms(self):
    terms = Term.objects.all()
    available_terms = []

    for term in terms:
        if datetime.date.today() <= term.end_date:
            available_terms.append(term)

    return available_terms