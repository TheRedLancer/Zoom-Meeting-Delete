"""Zoom Recording Management"""
# recordingDelete.py
# Author: Zach Burnaby (mailto:zachary.burnaby@kennedyhs.org)
# Project: Zoom Recording Management
# Last Modified: 2020-09-15
#
# Purpose: 
# This program will delete meeting recordings given
# a daterange. It asks the Zoom api for a list of meetings
# within the given daterange and for each meeting, sends
# a delete request to Zoom's api 
#
# Contributors: Zach Burnaby
#
# Imports: API, json
#
# Functions defined: jprint(obj), delete_meeting(API_KEY, API_SECRET, meeting_UUID)
#
#
#


import API
import json

def jprint(obj):
    # Create and print string of JSON Object
    # Grabbed from "https://www.dataquest.io/blog/python-api-tutorial/"
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def delete_meeting(API_KEY, API_SECRET, meeting_UUID):
    error_message = ""

    # Request delete
    n = API.deleteMeetingRecordings(API_KEY, API_SECRET, meeting_UUID)

    if n.status_code >= 400:
        error_message = n.json()["message"]

    # Print MeetingID and API Response
    print("[DELETE] ", meeting_UUID, n, error_message)


with open("APIKey.jwt", "r") as jwt_file:
    JWT = jwt_file.read().splitlines()
API_KEY = JWT[0]
API_SECRET = JWT[1]

start_date = "2020-09-02"
end_date = "2020-09-03"

next_page_token = ""

# Simulate a do-while loop
first_call = True

while ((first_call == True) or (next_page_token != "")):
    first_call = False

    # Make API call to get the next meeting in the date range
    response = API.getAccountRecordings(
        API_KEY, API_SECRET, 'me', start_date, end_date, next_page_token)

    # Convert API response to JSON
    api_recording = response.json()

    # Print API response
    jprint(api_recording)

    next_page_token = api_recording["next_page_token"]

    # Print Meeting Data
    print("[GET]    ", api_recording["meetings"][0]["uuid"], response,
          api_recording["meetings"][0]["host_email"],
          api_recording["meetings"][0]["topic"])

    # Do not delete meetings from "kchszoom"
    if api_recording["meetings"][0]["host_email"] != "kchszoom@kennedyhs.org":
        delete_meeting(API_KEY, API_SECRET, api_recording["meetings"][0]["uuid"])

print("Job Complete")