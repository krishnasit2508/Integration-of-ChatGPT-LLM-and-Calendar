import os.path

from google.auth.transport import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def schedule_meeting(summary, description, startTime, endTime):
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("tokenCal.json"):
    creds = Credentials.from_authorized_user_file("tokenCal.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(requests())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "/Users/krishnasit/Downloads/finalProject/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("tokenCal.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)
    event = {
    'summary': summary,
    'location': 'Google Meet',
    'description': description,
    'start': {
        'dateTime': startTime,
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': endTime,
        'timeZone': 'America/Los_Angeles',
    },
    }

    # Call the Calendar API to create the event
    created_event = service.events().insert(calendarId='primary', body=event).execute()

    eventResponse = created_event.get('htmlLink');
    return ('Event created: %s' % eventResponse)

  except HttpError as error:
    return(f"An error occurred: {error}")