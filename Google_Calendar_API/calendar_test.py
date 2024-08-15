from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from beautiful_date import *
from gcsa.attendee import Attendee
from datetime import date
import os
from dotenv import load_dotenv


load_dotenv()
#always go to the google developer console

MONTHS = {
    "Jan":Jan,
    "Feb":Feb,
    "Mar":Mar,
    "Apr":Apr,
    "May":May,
    "Jun":Jun,
    "Jul":Jul,
    "Aug":Aug,
    "Sep":Sept,
    "Oct":Oct,
    "Nov":Nov,
    "Dec":Dec
}
calendar = GoogleCalendar(os.environ.get('email'),credentials_path=r"Google_Calendar_API\credentials\client_secret_700876677420-vnos9h7oo954mb3atv4f8mgtsm51asth.apps.googleusercontent.com.json")
# for event in calendar:
#     print(event)

def show_upcoming_events():
    for event in calendar:
        print(event)

    return [event for event in calendar]

# attendee = Attendee(
#     'ds27801@georgiasouthern.edu',
#     additional_guests=3
# )

def add_attendee(email):
    attendee = Attendee(
        email,
        additional_guests=3
    )
    return attendee

# event = Event(
#     'sleep',
#     start=(15 / Aug / 2024)[9:00],
#     attendees=attendee
# )
# calendar.add_event(event)



def create_event(title,date,hour,attendee=None):
    date = date.split("/")
    event = Event(
        title,
        start=(int(date[0])/MONTHS[date[1]]/int(date[2]))[hour:00],
        attendees=attendee,
        color_id=11
    )
    calendar.add_event(event)



# show_upcoming_events()


# create_event("flag football","16/Aug/2024",10,attendee=add_attendee("ds27801@georgiasouthern.edu"))

####Super helpful getting google api console to work
#https://stackoverflow.com/questions/11485271/google-oauth-2-authorization-error-redirect-uri-mismatch
#https://stackoverflow.com/questions/62043149/google-calendar-create-event-says-successful-but-not-showing-on-calendar