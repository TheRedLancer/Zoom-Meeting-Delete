"""USED FOR ZBURNABY TO TEST"""
# This file will be deleted when I post Version 1.0
# I use this to test python code without modifying my working file
# It probably isn't the best practice as I should learn about Git branches

import API
import json
import urllib.parse as urllib


def jprint(obj):
    # Create and print string of JSON Object
    # Grabbed from "https://www.dataquest.io/blog/python-api-tutorial/"
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


with open("APIKey.jwt", "r") as jwt_file:
    JWT = jwt_file.read().splitlines()

API_KEY = JWT[0]
API_SECRET = JWT[1]

start_date = "2020-08-20"
endDate = "2020-08-26"

meetingsToDelete = []

# Make first call
r = API.getAccountRecordings(
    API_KEY, API_SECRET, 'me', start_date, endDate, "")

# Convert response to JSON
apiRecording = r.json()

# Print returned call
# jprint(apiRecording)

# Set next page token variable
next_page_token = apiRecording['next_page_token']

# Don't delete kchszoom recordings
if apiRecording["meetings"][0]["host_email"] == "kchszoom@kennedyhs.org":
    # Append Meeting ID to meetingsToDelete
    meetingsToDelete.append(apiRecording["meetings"][0]["uuid"])

# Print Meeting Data
print(apiRecording["meetings"][0]["uuid"], r,
      apiRecording["meetings"][0]["host_email"],
      apiRecording["meetings"][0]["topic"])

while next_page_token != '':
    # Make sequential call with next page token from prev call
    apiRecording = API.getAccountRecordings(
        API_KEY, API_SECRET, 'me', start_date, endDate, next_page_token).json()

    # Print returned call (debugging)
    # jprint(apiRecording)

    # Set next page token variable
    next_page_token = apiRecording['next_page_token']

    # If the name of the user is not the school's account, append the MeetingID to the delete queue
    if apiRecording["meetings"][0]["host_email"] == "kchszoom@kennedyhs.org":
        # Append Meeting ID to meetingsToDelete
        meetingsToDelete.append(apiRecording["meetings"][0]["uuid"])

    # Print Meeting Data
    print(apiRecording["meetings"][0]["uuid"], r,
          apiRecording["meetings"][0]["host_email"],
          apiRecording["meetings"][0]["topic"])

# print(meetingsToDelete)

print("Number of meetings to delete:", len(meetingsToDelete))


def deleteMeeting(API_KEY, API_SECRET, meetingUUID):
    # Request delete
    n = API.deleteMeetingRecordings(API_KEY, API_SECRET, meetingUUID)
    # Print MeetingID and API Response
    print(meetingUUID, n)


def deleteMeetings(API_KEY, API_SECRET, meetingsToDelete):
    for meeting in meetingsToDelete:
        # Request delete
        n = API.deleteMeetingRecordings(API_KEY, API_SECRET, meeting)
        # Print MeetingID and API Response
        print(meeting, n)


# Delete all meetings in the meetingsToDelete array
#deleteMeetings(API_KEY, API_SECRET, meetingsToDelete)
for meeting in meetingsToDelete:
    print(urllib.quote_plus(meeting))


jwt_file.close()
