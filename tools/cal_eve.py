from calender import GCalender
import datetime

cal = GCalender()

def parse_input(input_str):
    try:
        year, month, day, hour, minute = map(int, input_str.split(','))
        dt = datetime.datetime(year, month, day, hour, minute)
        return dt
    except ValueError:
        return None

def event(start_str: str, end_str: str):
    # Parse the start and end times using the parse_input function
    start_time = parse_input(start_str)
    end_time = parse_input(end_str)

    if start_time and end_time:
        events = {
            'summary': 'Sayvai IO',
            'location': 'Coimbatore, Tamil Nadu, India',
            'description': 'Sayvai IO is a startup company',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'IST',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'IST',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'attendees': [
                {'email': 'athikabilanvenkatesan@sayvai.io'},
                {'email': 'kedareeshwarsekar@sayvai.io'}
            ]
        }
        return cal.create_event(events)
    else:
        return None

print(event('2023,10,20,13,30', '2023,10,20,14,00'))