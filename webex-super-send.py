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
    url = "https://webexapis.com/v1/messages/"
    response = request("POST", url, data=json.dumps(kwargs),
                       headers=WEBEX_HEADERS)
    return response.status_code


# -----------------------------------------------------------------------------
# ARGPARSE

parser = argparse.ArgumentParser(
    description='Send a message or card through Webex.')
parser.add_argument('--message', '-m', metavar='FILE',
                    help='File containing message to be sent.')
parser.add_argument(
    '--token', '-t', help='Webex token if not stored as WEBEX_TOKEN environment variable.')
parser.add_argument(
    'recipients', help='List of emails or rooms to send to.', nargs='*')
args = parser.parse_args()

# The Webex token to be used must either be set as an environment variable or
# specified as a command-line argument (higher priority than the environment
# variable). The Webex header is created using the given token.
if args.token is None and os.getenv('WEBEX_TOKEN') is None:
    print('\nERROR! You must specify a WEBEX API token to send any messages.')
    print('You can specify at the command line or set it as an environment variable called WEBEX_TOKEN.\n')
    parser.print_help()
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

# The user must specify a message (card or markdown) in a file.
if args.message is None:
    print('ERROR! You did not specify a message to send.\n')
    parser.print_help()
    exit(0)


# -----------------------------------------------------------------------------
# CHECK MESSAGE PAYLOAD

# If message is valid JSON, it is assumed to be an adaptive card and a
# markdown message is created as a fallback if the client cannot render the
# card.
# If it is not valid JSON, it is assumed to be a markdown message. An empty
# list is created as an attachment.
# In either case, this block of code creates the variables markdown and
# attachments. Both variables are used later for every send operation.

with open(args.message, 'r') as file:
    try:
        # wrap the JSON from the card designer in the required JSON envelope
        attachments = dict(
            contentType="application/vnd.microsoft.card.adaptive",
            content=json.load(file)
        )
        markdown = "*Card could not be rendered*"
    except:
        file.seek(0)
        attachments = []
        markdown = file.read()

# -----------------------------------------------------------------------------
# MAIN

# If a target has an @, it is assumed to be an email address and the message
# will be sent to an email. Otherwise, it is assumed to be the ID of a room or
# space, so it will be sent to that roomId.

for target in args.recipients:

    if '@' in target:
        my_args = dict(toPersonEmail=target)
    else:
        my_args = dict(roomId=target)

    # use the same attachments and markdown for every target
    my_args['attachments'] = attachments
    my_args['markdown'] = markdown

    status = send_webex_message(**my_args)
    print(F'status {status}: {target}')
