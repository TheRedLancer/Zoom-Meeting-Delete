import requests
import json
import jwt
from time import time
import secrets

# create a function to generate a token using the pyjwt library
# Copied from https://devforum.zoom.us/t/zoom-jwt-token-creation-automate-the-process/17708 Code by user michael.harrington
def generateToken(API_KEY, API_SECRET):
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

def getUsers(API_KEY, API_SECRET, userID = ''): 
    headers = {'authorization': 'Bearer %s' % generateToken(API_KEY, API_SECRET),
               'content-type': 'application/json'}
    querystring = {"page_number":"3","page_size": "3"}

    r = requests.get('https://api.zoom.us/v2/users/' + userID, headers=headers, params=querystring)

    return(r)

def getAccountRecordings(API_KEY, API_SECRET, accountID, fromDate, toDate, nextPageToken = ''):
    headers = {'authorization': 'Bearer %s' % generateToken(API_KEY, API_SECRET),
               'content-type': 'application/json'}

    querystring = {"page_size":"1", "from": fromDate, "to": toDate, "next_page_token": nextPageToken}

    r = requests.get('https://api.zoom.us/v2/accounts/' + accountID + "/recordings", params= querystring, headers=headers)

    return(r)

