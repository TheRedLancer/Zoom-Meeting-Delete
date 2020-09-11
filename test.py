
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

print(API_KEY + API_SECRET)
jprint(API.getUsers(API_KEY,API_SECRET).json())

jwtFile.close()