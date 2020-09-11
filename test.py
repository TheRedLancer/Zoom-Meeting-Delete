
import API
import json


def jprint(obj):
    # Create and print string of JSON Object
    # Grabbed from "https://www.dataquest.io/blog/python-api-tutorial/"
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


with open("APIKey.jwt", "r") as jwtFile:
    JWT = jwtFile.read().splitlines()

API_KEY = JWT[0]
API_SECRET = JWT[1]

#jprint(API.getUsers(API_KEY,API_SECRET, "EboregvTQKyB6e-q2jlFpQ").json())

jprint(API.getAccountRecordings(API_KEY, API_SECRET, 'me', "2020-08-12",
                                "2020-08-29", "N4erQu8Jt1t3LW0JdSwFOFjMADKS6OgzHp2").json())

jwtFile.close()
