"""Zoom API Interface"""
# API.py
# Author: Zach Burnaby (mailto:zachary.burnaby@kennedyhs.org)
# Project: Zoom Recording Management
# Last Modified: 2020-09-16
#
# Purpose: 
# This provides helper functions for connectivity to api.zoom.us for
# recordingDelete.py using the requests library.
#
# Contributors: Zach Burnaby
#
# Imports: requests, json, jwt, time, secrets
#
# Functions defined: generateToken(), getUsers(), getAccountRecordings()
# getUserRecordings(), deleteMeetingRecordings(), updateUserFirstName()
# postUserProfilePicture()
#  

import requests
import json
import jwt
from time import time
import secrets

# create a function to generate a token using the pyjwt library
# Copied from https://devforum.zoom.us/t/zoom-jwt-token-creation-automate-the-process/17708 
# Code by user michael.harrington

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


def getUsers(API_KEY, API_SECRET, userID=''):
    headers = {'authorization': 'Bearer %s' % generateToken(API_KEY, API_SECRET),
               'content-type': 'application/json'}
    querystring = {"page_number": "1", "page_size": "3"}

    r = requests.get('https://api.zoom.us/v2/users/' + userID,
                     headers=headers, params=querystring)

    return(r)


def getAccountRecordings(API_KEY, API_SECRET, accountID, fromDate, toDate, nextPageToken=''):
    headers = {'authorization': 'Bearer %s' % generateToken(API_KEY, API_SECRET),
               'content-type': 'application/json'}

    querystring = {"page_size": "300", "from": fromDate,
                   "to": toDate, "next_page_token": nextPageToken}

    r = requests.get('https://api.zoom.us/v2/accounts/' + accountID +
                     "/recordings", headers=headers, params=querystring)

    return(r)


def getUserRecordings(API_KEY, API_SECRET, userID, fromDate, toDate, nextPageToken=''):
    headers = {'authorization': 'Bearer %s' % generateToken(API_KEY, API_SECRET),
               'content-type': 'application/json'}

    querystring = {"page_size": "1", "from": fromDate,
                   "to": toDate, "next_page_token": nextPageToken}

    r = requests.get('https://api.zoom.us/v2/users/' + userID +
                     "/recordings", headers=headers, params=querystring)

    return(r)


def deleteMeetingRecordings(API_KEY, API_SECRET, meetingID, action="trash"):
    headers = {'authorization': 'Bearer %s' % generateToken(API_KEY, API_SECRET),
               'content-type': 'application/json'}

    querystring = {"action": action}

    r = requests.delete('https://api.zoom.us/v2/meetings/' + str(meetingID) +
                        "/recordings", headers=headers, params=querystring)

    return(r)


def updateUserFirstName(API_KEY, API_SECRET, userID, newFirstName):
    headers = {'authorization': 'Bearer %s' % generateToken(API_KEY, API_SECRET),
               'content-type': 'application/json'}
    querystring = {"login_type": "101"}

    payload = "{\"first_name\":\"" + newFirstName + "\"}"

    r = requests.patch('https://api.zoom.us/v2/users/' + str(userID), data=payload,
                       headers=headers, params=querystring)

    return(r)

"""
def postUserProfilePicture(API_KEY, API_SECRET, userID):
    headers = {'authorization': 'Bearer %s' % generateToken(API_KEY, API_SECRET),
               'content-type': 'multipart/form-data'}

    file = {"pic_file": open("kennedySeal.png", 'rb')}

    r = requests.post("https://api.zoom.us/v2/users/me/picture", headers=headers, files=file)

    return(r)
"""
