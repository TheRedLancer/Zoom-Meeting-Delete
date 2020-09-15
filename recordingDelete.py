import API
import json

def jprint(obj):
    # Create and print string of JSON Object
    # Grabbed from "https://www.dataquest.io/blog/python-api-tutorial/"
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def deleteMeeting(API_KEY, API_SECRET, meetingUUID):
    # Request delete
    n = API.deleteMeetingRecordings(API_KEY, API_SECRET, meetingUUID)

    if n.status_code >= 400:
        errorMessage = n.json()["message"]

    # Print MeetingID and API Response
    print("[DELETE] ", meetingUUID, n, errorMessage)

with open("APIKey.jwt", "r") as jwtFile:
    JWT = jwtFile.read().splitlines()
API_KEY = JWT[0]
API_SECRET = JWT[1]

startDate = "2020-09-02"
endDate = "2020-09-03"

meetingToDelete = ""
next_page_token = ""

# Simulate a do-while loop
firstCall = True


while ((firstCall == True) or (next_page_token != "")):
    firstCall = False

    # Make API call to get the next meeting in the date range
    response = API.getAccountRecordings(
        API_KEY, API_SECRET, 'me', startDate, endDate, next_page_token)

    # Convert API response to JSON
    apiRecording = response.json()

    # Print API response
    jprint(apiRecording)

    next_page_token = apiRecording["next_page_token"]

    # Print Meeting Data
    print("[GET]    ", apiRecording["meetings"][0]["uuid"], response,
          apiRecording["meetings"][0]["host_email"],
          apiRecording["meetings"][0]["topic"])

    # Do not delete meetings from "kchszoom"
    if apiRecording["meetings"][0]["host_email"] != "kchszoom@kennedyhs.org":
        deleteMeeting(API_KEY, API_SECRET, apiRecording["meetings"][0]["uuid"])

print("Job Complete")