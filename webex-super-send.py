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
# FUNCTIONS

def send_webex_message(**kwargs):
    """Sends a Webex message using kwargs so that it can send markdown or cards
    to either a person's email or a roomId. Returns status code of the call."""
    # payload = dict(toPersonEmail=email, markdown=message)
    url = "https://webexapis.com/v1/messages/"
    response = request("POST", url, data=json.dumps(kwargs),
                       headers=WEBEX_HEADERS)
    return response.status_code


# -----------------------------------------------------------------------------
# ARGPARSE

parser = argparse.ArgumentParser(description='Send a message or card through Webex.')
parser.add_argument('--message', '-m', help='File containing message to be sent.')
parser.add_argument('--token', help='Webex token if not stored as WEBEX_TOKEN environment variable.')
parser.add_argument('recipients', help='List of emails or rooms to send to.', nargs='*')
args = parser.parse_args()

if args.token is None and os.getenv('WEBEX_TOKEN') is None:
    print('\nERROR! You must specify a WEBEX API token to send any messages.')
    print('You can specify at the command line or set it as an environment variable called WEBEX_TOKEN.\n')
    exit(0)
elif args.token is not None:
    WEBEX_HEADERS = {
            "Authorization": "Bearer " + args.token,
            "Content-Type": "application/json"
        }
else:
    WEBEX_HEADERS = {
            "Authorization": "Bearer " + os.environ['WEBEX_TOKEN'],
            "Content-Type": "application/json"
        }

if args.message is None:
    print('ERROR! You did not specify a message to send.\n')
    parser.print_help()
    exit(0)


# -----------------------------------------------------------------------------
# CHECK PAYLOAD

# If payload is valid JSON, it is assumed to be an adaptive card. Otherwise it
# is assumed to be a markdown message. The boolean 'is_card' is set to track
# whether the message payload is a card.

with open(args.message, 'r') as file:
    try:
        payload = dict(contentType="application/vnd.microsoft.card.adaptive",
                       content=json.load(file))
        is_card = True
    except:
        file.seek(0)
        payload = file.read()
        is_card = False

# -----------------------------------------------------------------------------
# MAIN

for target in args.recipients:
    my_args = dict()
    if is_card:
        my_args['attachments'] = payload
        my_args['markdown'] = 'Card could not be displayed.'
    else:
        my_args['markdown'] = payload

    if '@' in target:
        my_args['toPersonEmail'] = target
    else:
        my_args['roomId'] = target

    status = send_webex_message(**my_args)
    print(F'status {status}: {target}')
