# event = {
#   'summary': 'Google I/O 2025',
#   'location': '800 Howard St., San Francisco, CA 94103',
#   'description': 'A chance to hear more about Google\'s developer products.',
#   'start': {
#     'dateTime': '2025-05-28T09:00:00-07:00',
#     'timeZone': 'America/Los_Angeles',
#   },
#   'end': {
#     'dateTime': '2025-05-28T17:00:00-07:00',
#     'timeZone': 'America/Los_Angeles',
#   },
#   'reminders': {
#     'useDefault': False,
#     'overrides': [
#       {'method': 'email', 'minutes': 24 * 60},
#       {'method': 'popup', 'minutes': 10},
#     ],
#   },
# }

from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class DailyPlanner:
    def __init__(self):
        """Initializes the Google Calendar API and gets the service."""
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)

    def get_upcoming_events(self):
        """Gets the upcoming 10 events on the user's calendar."""
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        return events

    def create_event(
        self, start_time, end_time, summary, description=None, location=None
    ):
        """
        Creates an event.

        :param start_time: str, start time in the format '2023-05-26T15:00:00-07:00'
        :param end_time: str, end time in the same format as start_time
        :param summary: str, event title
        :param description: str, event description
        :param location: str, location of the event
        """
        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": "America/Los_Angeles",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "America/Los_Angeles",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        event = self.service.events().insert(calendarId="primary", body=event).execute()
        print(f'Event created: {event["htmlLink"]}')

    def update_event(
        self,
        event_id,
        start_time=None,
        end_time=None,
        summary=None,
        description=None,
        location=None,
    ):
        """
        Updates an event.

        :param event_id: str, the ID of the event to update
        :param start_time: str, start time in the format '2023-05-26T15:00:00-07:00'
        :param end_time: str, end time in the same format as start_time
        :param summary: str, event title
        :param description: str, event description
        :param location: str, location of the event
        """
        event = (
            self.service.events().get(calendarId="primary", eventId=event_id).execute()
        )

        if start_time:
            event["start"]["dateTime"] = start_time
        if end_time:
            event["end"]["dateTime"] = end_time
        if summary:
            event["summary"] = summary
        if description:
            event["description"] = description
        if location:
            event["location"] = location

        updated_event = (
            self.service.events()
            .update(calendarId="primary", eventId=event_id, body=event)
            .execute()
        )
        print(f'Event updated: {updated_event["htmlLink"]}')

    def delete_event(self, event_id):
        """
        Deletes an event.

        :param event_id: str, the ID of the event to delete
        """
        try:
            self.service.events().delete(
                calendarId="primary", eventId=event_id
            ).execute()
            print("Event deleted.")
        except googleapiclient.errors.HttpError:
            print("Failed to delete event.")

    def console_interaction(self):
        """Console-based interaction for managing Google Calendar events."""
        print("Welcome to Daily Planner")
        while True:
            print("1. View upcoming events")
            print("2. Add an event")
            print("3. Update an event")
            print("4. Delete an event")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                events = self.get_upcoming_events()
                if not events:
                    print("No upcoming events found.")
                else:
                    for event in events:
                        start = event["start"].get(
                            "dateTime", event["start"].get("date")
                        )
                        print(start, event["summary"])
            elif choice == "2":
                # Prepare and add an event here
                print("Functionality not implemented yet.")
            elif choice == "3":
                # Update an event here
                print("Functionality not implemented yet.")
            elif choice == "4":
                # Delete an event here
                print("Functionality not implemented yet.")
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    planner = DailyPlanner()
    planner.console_interaction()
