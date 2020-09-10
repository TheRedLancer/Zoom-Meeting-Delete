import requests
import json
import jwt
from time import time
import secrets

def jprint(obj):
    # Create and print string of JSON Object
    # Grabbed from "https://www.dataquest.io/blog/python-api-tutorial/"
    text = json.dumps(obj, sort_keys=True, indent = 4)
    print(text)

API_KEY = "API KEY HERE"

API_SECRET = "API SECRET HERE"

# create a function to generate a token using the pyjwt library
# Copied from https://devforum.zoom.us/t/zoom-jwt-token-creation-automate-the-process/17708 Code by user michael.harrington
def generateToken():
    token = jwt.encode(
        # Create a payload of the token containing API Key & expiration time
        {"iss": API_KEY, "exp": time() + 5000},
        # Secret used to generate token signature
        API_SECRET,
        # Specify the hashing alg
        algorithm='HS256'
        # Convert token to utf-8
    ).decode('utf-8')

    return token

def getUsers(): 
    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}

    r = requests.get('https://api.zoom.us/v2/users/', headers=headers)

    return(r)

def getMeetings():
    headers = {'authorization': 'Bearer %s' % generateToken(),
               'content-type': 'application/json'}

    r = requests.get('https://api.zoom.us/v2/meetings', headers=headers)

    return(r)

jprint(getMeetings().json())