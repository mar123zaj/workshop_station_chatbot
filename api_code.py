from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import datefinder
import datetime
import pprint
from random import randint


GMT_OFFSET = "+02:00"
TIME_ZONE = "Europe/Kaliningrad"
LINE_LENGTH = 25

OPEN_HOURS = {
    "Monday": "9:00 - 17:00",
    "Tuesday": "9:00 - 17:00",
    "Wednesday": "9:00 - 17:00",
    "Thursday": "9:00 - 17:00",
    "Friday": "9:00 - 17:00",
    "Saturday": "9:00 - 13:00",
}
OPEN_HOURS_DICT = {
    "Monday": {"start": 9, "end": 17},
    "Tuesday": {"start": 9, "end": 17},
    "Wednesday": {"start": 9, "end": 17},
    "Thursday": {"start": 9, "end": 17},
    "Friday": {"start": 9, "end": 17},
    "Saturday": {"start": 9, "end": 13},
}

SERVICES_TIME_NEEDED = {
    "light-bulb": {"hours": 0, "minutes": 15},
    "oil": {"hours": 1, "minutes": 0},
    "tyres": {"hours": 0, "minutes": 30},
    "repair": {"hours": 0, "minutes": 10},
}

SERVICES_PRICING = {
    "light-bulb": "$20",
    "oil": "$35",
    "tyres": "$50",
    "repair": "priced individually",
}


def open_hours(google_calendar_date):
    """ Get working hours of given day,
        if given string is empty, just return all week working hours


        If we could have Google Places API we could get
        working days through this.
    """

    dates = datefinder.find_dates(google_calendar_date)

    for date in dates:
        final_date = datetime.datetime(
            date.year, date.month, date.day, date.hour, date.minute
        )
        weekday = final_date.strftime("%A")
        if weekday != "Sunday":
            return f"Our working hours on {weekday}: {OPEN_HOURS[weekday]}."
        else:
            return "Unfortunately we're closed on Sundays."
    else:
        all_open_hours = "Our working hours on specific days: <br>"
        for weekday, hours in OPEN_HOURS.items():
            length = len(weekday)
            hours_formatted = hours.rjust(LINE_LENGTH - length, chr(32))
            all_open_hours += f"{weekday} {hours_formatted}<br>"
        return f"<pre>{all_open_hours}</pre>"


def get_service_pricing(service):
    """This is function could get data through API from
        third party application"""
    return SERVICES_PRICING[service]


def pricing(service):
    if service == "":
        response = "Our pricing: <br>"
        for service, price in SERVICES_PRICING.items():
            if service != "repair":
                length = len(service)
                price_formatted = price.rjust(15 - length, chr(32))
                response += f"Change {service} {price_formatted}<br>"
            else:
                response += "Non-standard repairs are priced individually."
        return f"<pre>{response}</pre>"
    elif service == "repair":
        return "Non-standard repairs are priced individually."
    else:
        price = get_service_pricing(service)
        return f"Change {service} will cost {price}."


def add_time_offset(date_time, hours, minutes):
    dates = datefinder.find_dates(date_time)
    for date in dates:
        final_date = datetime.datetime(
            date.year, date.month, date.day, date.hour + hours, date.minute + minutes
        )
        return final_date.strftime(f"%Y-%m-%dT%H:%M:%S{GMT_OFFSET}")


def client_date_format(date_time):
    dates = datefinder.find_dates(date_time)
    for date in dates:
        final_date = datetime.datetime(
            date.year, date.month, date.day, date.hour, date.minute
        )
    return final_date.strftime("%#d %B at %H:%M")


def list_events():
    SCOPES = "https://www.googleapis.com/auth/calendar"
    store = file.Storage("storage.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    GCAL = discovery.build("calendar", "v3", http=creds.authorize(Http()))
    events = GCAL.events().list(calendarId="primary", timeZone=TIME_ZONE).execute()
    return events["items"]


def formatted_date(date_time):
    dates = datefinder.find_dates(date_time)
    for date in dates:
        return datetime.datetime(
            date.year, date.month, date.day, date.hour, date.minute
        )


def event_available(input_start_date, input_end_date):
    events = list_events()
    start_date = formatted_date(input_start_date)
    end_date = formatted_date(input_end_date)
    for event in events:
        start = formatted_date(event["start"]["dateTime"])
        end = formatted_date(event["end"]["dateTime"])
        if start <= start_date < end or start < end_date <= end:
            return False
        else:
            continue
    return True


def set_appointment(service_type, start_date_time, end_date_time):
    SCOPES = "https://www.googleapis.com/auth/calendar"
    store = file.Storage("storage.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    try:
        GCAL = discovery.build("calendar", "v3", http=creds.authorize(Http()))
    except Exception:
        return "Exception"

    if event_available(start_date_time, end_date_time):
        body = {
            "summary": service_type,
            "start": {f"dateTime": start_date_time},
            "end": {f"dateTime": end_date_time},
            "attendees": [{"email": "companyNotificatonEmail@example.com"}],
        }
        try:
            event = (
                GCAL.events()
                .insert(calendarId="primary", sendNotifications=True, body=body)
                .execute()
            )
        except Exception:
            return "Exception"
        return "Successful"
    else:
        return "Availability problem"


def merge_date_time(date, time):
    dates = datefinder.find_dates(date)
    times = datefinder.find_dates(time)
    for date in dates:
        year = date.year
        month = date.month
        day = date.day
        break
    for time in times:
        minute = time.minute
        hour = time.hour
        break
    final_date = datetime.datetime(year, month, day, hour, minute)
    return final_date.strftime(f"%Y-%m-%dT%H:%M:%S{GMT_OFFSET}")


def appointment(service_type, start_date, time):
    start_date_time = merge_date_time(start_date, time)
    end_date_time = add_time_offset(
        start_date_time,
        SERVICES_TIME_NEEDED[service_type]["hours"],
        SERVICES_TIME_NEEDED[service_type]["minutes"],
    )
    appointment_status = set_appointment(service_type,
                                         start_date_time,
                                         end_date_time
                                         )
    if appointment_status == "Successful":
        display_start_date = client_date_format(start_date_time)
        display_end_date = client_date_format(end_date_time)
        result = "Everything went well, I set appointment for " \
                 f"{service_type} at {display_start_date}"
        if service_type != "repair":
            return f"{result}. " \
                   f"Our mechanics will need time till {display_end_date}"
        else:
            return f"{result}. Notice that you chosed non-standard repair," \
                    " so you will only need to leave your car."
    elif appointment_status == "Exception":
        return "We encountered some unexpected problem. " \
               "Please try again after few minutes."
    elif appointment_status == "Availability problem":
        return "There is already appointment for this time, " \
                "please choose another time." \
                "I can help you with that, just type \"available hours\"."


def google_date_format(date):
    return date.strftime(f"%Y-%m-%dT%H:%M:%S+00:00")


def available_hours(service_type, date_time):
    if service_type == "":
        service_type = "oil"
    counter_propositions = 5
    response = "What do you say about this hours?<br>"
    date = formatted_date(date_time)
    weekday = date.strftime("%A")
    open_hour = OPEN_HOURS_DICT[weekday]["start"]
    close_hour = OPEN_HOURS_DICT[weekday]["end"]
    start_date = datetime.datetime(date.year, date.month,
                                   date.day, open_hour
                                   )
    end_date = datetime.datetime(date.year, date.month,
                                 date.day, close_hour
                                 )
    while start_date != end_date:
        sercice_end_date = datetime.datetime(
            start_date.year,
            start_date.month,
            start_date.day,
            start_date.hour + SERVICES_TIME_NEEDED[service_type]["hours"],
            start_date.minute + SERVICES_TIME_NEEDED[service_type]["minutes"],
        )

        event_start_date = google_date_format(start_date)
        event_end_date = google_date_format(sercice_end_date)
        if event_available(event_start_date, event_end_date):
            response += start_date.strftime("%#d %B at %H:%M") + "<br>"
            counter_propositions -= 1
        start_date = datetime.datetime(
            start_date.year, start_date.month,
            start_date.day, start_date.hour + 1
        )
    return response + "Remember to set appointment, " \
           "just write me which date and time you prefer, " \
           "and I will set an appointment for you."



