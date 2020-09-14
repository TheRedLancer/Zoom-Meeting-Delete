
import API
import json

def jprint(obj):
    # Create and print string of JSON Object
    # Grabbed from "https://www.dataquest.io/blog/python-api-tutorial/"
    text = json.dumps(obj, sort_keys=True, indent = 4)
    print(text)

with open("APIKey.jwt", "r") as jwtFile:
    JWT = jwtFile.read().splitlines()

API_KEY = JWT[0]
API_SECRET = JWT[1]

meetingsToDelete = []

startDate = "2020-08-20"
endDate = "2020-08-24"

# Make first call
apiRecording = API.getAccountRecordings(API_KEY, API_SECRET, 'me', startDate, endDate, "").json()
# Print returned call
#jprint(apiRecording)
# Set next page token variable
next_page_token = apiRecording['next_page_token']
# Append Meeting ID to meetingsToDelete
meetingsToDelete.append(apiRecording["meetings"][0]["id"])
# Print Meeting ID
print(apiRecording["meetings"][0]["id"])
# Line Break
print("-------------------------------------------------")

while next_page_token != '':
    # Make sequential call with next page token from prev call
    apiRecording = API.getAccountRecordings(API_KEY, API_SECRET, 'me', "2020-08-20", "2020-08-24", next_page_token).json()
    # Print returned call
    #jprint(apiRecording)
    # Set next page token variable
    next_page_token = apiRecording['next_page_token']
    # Append Meeting ID to meetingsToDelete
    meetingsToDelete.append(apiRecording["meetings"][0]["id"])
    # Print MeetingID
    print(apiRecording["meetings"][0]["id"])
    # Line Break
    print("-------------------------------------------------")

print(meetingsToDelete)

print(meetingsToDelete[0])
n = API.deleteMeetingRecordings(API_KEY, API_SECRET, meetingsToDelete[0], "delete")
print(n)
jwtFile.close()