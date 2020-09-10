import requests
import json
import jwt

from datetime import datetime

def jprint(obj):
    # Create and print string of JSON Object
    # Grabbed from "https://www.dataquest.io/blog/python-api-tutorial/"
    text = json.dumps(obj, sort_keys=True, indent = 4)
    print(text)

ROOT = "http://api.open-notify.org" # Root url for the api

endpoint = '/iss-pass.json'

headers = {
    'authorization': "PUT STUFF HERE", #YOU NEED THIS
    'content-type': "application/json"
}

perameters = {
    "lat": 40.71,
    "lon": -74
}

res = requests.get(ROOT + endpoint, perameters)

jprint(res.json())


"""
pass_times = res.json()['response']
print("Pass Times: ")
jprint(pass_times)

risetimes = []

for d in pass_times:
    time = d['risetime']
    risetimes.append(time)

print(risetimes)

times = []

for rt in risetimes:
    time = datetime.fromtimestamp(rt)
    times.append(time)
    print(time)
"""