"""Zoom Recording Management"""
# recordingDelete.py
# Author: Zach Burnaby (mailto:zachary.burnaby@kennedyhs.org)
# Project: Zoom Recording Management
# Last Modified: 2020-09-16
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
# Functions defined: jprint(), delete_meeting(), double_encode
#

import API
import json

def jprint(obj):
    # Create and print string of JSON Object
    # Grabbed from "https://www.dataquest.io/blog/python-api-tutorial/"
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def double_encode(uuid):
    newUUID = ""
    for c in uuid:
        if c == "/":
            newUUID += "%252F"
        elif c == "=":
            newUUID += "%253D"
        elif c == "+":
            newUUID += "%252B"
        else:
            newUUID += c
    return newUUID

def delete_meeting(API_KEY, API_SECRET, meeting_UUID):
    error_message = ""

    # Request delete
    n = API.deleteMeetingRecordings(API_KEY, API_SECRET, double_encode(meeting_UUID))

    if n.status_code >= 400:
        error_message = n.json()["message"]

    # Print MeetingID and API Response
    print("[DELETE] ", meeting_UUID, n, error_message)



with open("APIKey.jwt", "r") as jwt_file:
    JWT = jwt_file.read().splitlines()
API_KEY = JWT[0]
API_SECRET = JWT[1]

start_date = "2020-08-01"
end_date = "2020-09-03"

# Make API call to get meetings in the date range
response = API.getAccountRecordings(
        API_KEY, API_SECRET, 'me', start_date, end_date)

# Convert API response to JSON
response_json = response.json()

# Print API Response
# jprint(response_json)

for meeting in response_json["meetings"]:
    print("[GET]    ", meeting["uuid"], response,
            meeting["host_email"],
            meeting["topic"])

    # Do not delete meetings from "kchszoom"
    if meeting["host_email"] != "kchszoom@kennedyhs.org":
        #print("Delete UUID:", double_encode(meeting["uuid"]))
        delete_meeting(API_KEY, API_SECRET, meeting["uuid"])

print("Job Complete")
