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
# Functions defined: jprint(), delete_meeting(), double_encode()
#
# Future Features:
# TODO Make a whitelist for who to not delete
# TODO Add command line args for manually deleting date-range
# TODO Output metrics to CSV [meeting id, time of delete, errors, meeting host]

import API
import json


def jprint(obj):
    # Create and print string of JSON Object
    # Grabbed from "https://www.dataquest.io/blog/python-api-tutorial/"
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def double_encode(uuid):
    new_UUID = ""
    for c in uuid:
        if c == "/":
            new_UUID += "%252F"
        elif c == "=":
            new_UUID += "%253D"
        elif c == "+":
            new_UUID += "%252B"
        else:
            new_UUID += c
    return new_UUID


def delete_meeting(API_KEY, API_SECRET, meeting_UUID):
    error_message = ""

    # Request delete
    n = API.deleteMeetingRecordings(
        API_KEY, API_SECRET, double_encode(meeting_UUID))

    if n.status_code >= 400:
        error_message = n.json()["message"]

    # Print MeetingID and API Response
    print("[DELETE] ", meeting_UUID, n, error_message)


# Add users to this list you do NOT want meetings deleted
USER_WHITELIST = ["kchszoom@kennedyhs.org", "mohsm@kennedyhs.org"]

with open("APIKey.jwt", "r") as jwt_file:
    JWT = jwt_file.read().splitlines()
API_KEY = JWT[0]
API_SECRET = JWT[1]


start_date = "2020-09-08"
end_date = "2020-09-09"

# Make API call to get meetings in the date range
response = API.getAccountRecordings(
    API_KEY, API_SECRET, 'me', start_date, end_date)

# Convert API response to JSON
response_json = response.json()

# Print API Response
# jprint(response_json)
# next_page_token = response_json["next_page_token"]
print("Page Size  " + str(response_json["page_size"]))
print("Total Records  " + str(response_json["total_records"]))


for meeting in response_json["meetings"]:
    # Print ghost GET request and data
    print("[GET]    ", meeting["uuid"], response,
          meeting["host_email"],
          meeting["topic"])

    # if meeting["host_email"] == "":
    #    print(API.updateMeetingSettings(API_KEY, API_SECRET, meeting["uuid"]))
    # Do not delete meetings from whitelisted users
    if meeting["host_email"] not in USER_WHITELIST:
        # print("Delete UUID:", double_encode(meeting["uuid"]))
        delete_meeting(API_KEY, API_SECRET, meeting["uuid"])

print("Job Complete")


'''

# Make API call to get meetings in the date range
response = API.getUsers(API_KEY, API_SECRET)

# Convert API response to JSON
response_json = response.json()

# Print API Response
# jprint(response_json)
next_page_token = response_json["next_page_token"]
print("Page Size  " + str(response_json["page_size"]))
print("Total Records  " + str(response_json["total_records"]))


for user in response_json["users"]:
    res = API.postUserProfilePicture(API_KEY, API_SECRET, user["id"])
    print(res)

while next_page_token != '':
    # Make sequential call with next page token from prev call
    response = API.getUsers(API_KEY, API_SECRET, "", next_page_token)

    # Convert API response to JSON
    response_json = response.json()
    # Print returned call (debugging)
    # jprint(apiRecording)

    # Set next page token variable
    next_page_token = response_json['next_page_token']
    print("Page Size  " + str(response_json["page_size"]))
    print("Total Records  " + str(response_json["total_records"]))

    for user in response_json["users"]:
        res = API.postUserProfilePicture(API_KEY, API_SECRET, user["id"])
        print(res)

'''
