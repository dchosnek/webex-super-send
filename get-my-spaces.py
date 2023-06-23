"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Doron Chosnek"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


from requests import request
import json
import argparse
import os

# -----------------------------------------------------------------------------
# ARGPARSE

parser = argparse.ArgumentParser(description='Send a message or card through Webex.')
parser.add_argument('--all', action='store_true', help='This option will display all spaces, not just group spaces.')
parser.add_argument('-token', help='Webex token if not stored as WEBEX_TOKEN environment variable.')
args = parser.parse_args()

if args.token is None and os.getenv('WEBEX_TOKEN') is None:
    print('\nERROR! You must specify a WEBEX API token to send any messages.')
    print('You can specify at the command line or set it as an environment variable called WEBEX_TOKEN.\n')
    exit(0)
elif args.token is not None:
    WEBEX_HEADERS = {
            "Authorization": "Bearer " + args.token
        }
else:
    WEBEX_HEADERS = {
            "Authorization": "Bearer " + os.environ['WEBEX_TOKEN']
        }

if args.all:
    url = "https://webexapis.com/v1/rooms"
else:
    url = url = "https://webexapis.com/v1/rooms?type=group"

# -----------------------------------------------------------------------------
# MAIN

response = request("GET", url, data=dict(), headers=WEBEX_HEADERS)

print(json.dumps(response.json()['items'], indent=2))
