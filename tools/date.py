from datetime import datetime

def current_date(cur_date):
    """Get the current date"""
    current_datetime = datetime.now()
    # current_day = current_datetime.weekday()
    day_name = current_datetime.strftime('%A')
    return day_name, current_datetime
