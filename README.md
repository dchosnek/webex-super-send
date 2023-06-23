# Webex Super Send

This script will send an adaptive card *or* text message (markdown supported) in Webex to a list of recipients. That list can be a combination of user emails and identifiers for Webex rooms. In other words, with a single command, you can send the same message or card to multiple individuals and groups.

For those unfamiliar with Python, read the detailed [install](installation.md) instructions.

For those familiar with Python, simply clone this repo and `pip install -r requirements.txt`.

## General usage

To send a message contained in `FILE` to two users, execute the following:

```
python webex-super-send.py -m FILE user1@example.com user2@example.com
```

The script should hopefully respond with a status of `200` for each user like this:

```
status 200: user1@example.com
status 200: user2@example.com
```

**It is always a good idea to test a message by sending it to yourself!** Do this before sending a message to a large distribution list.

## Specifying the message

The message can be an adaptive card or a simple text message. In both cases, the contents of the message are stored in a file and specified at runtime with the `-m` commandline option. The message file is a required parameter.

The script automatically detects if file contains an adaptive card or just text.

### Adaptive card

To send an adaptive card, use the [Webex Card Designer](https://developer-portal-intb.ciscospark.com/buttons-and-cards-designer) and save the card payload to a file. It makes sense to give that file the `.json` extension, though it is not required by this script.

### Text

You can draft a simple or complex message in a text file. Webex supports markdown, so you can apply **bold** or *italics* within your message as well as using bullets and headings.

## Specifying the list of recipients

The list of people and groups who receive your message can be specified in two ways.

1. You can add emails or room IDs to the end of the command as shown here. This example will send the message to two users and one group whose ID has been truncated for readability.

```
python webex-super-send.py -m FILE user1@example.com user2@example.com Y2lzY29zcGF
```

2. You can specify the recipients by email or room ID in a text file (one per line) and use the `-l` option to reference the file.

```
python webex-super-send.py -m FILE -l mylist.txt
```

The file `mylist.txt` could look like this:

```
user1@example.com
user2@example.com
Y2lzY29zcGF
```

_NOTE_: You can specify recipients using **both** of the above mentioned methods and the script will send the notification to all recipients.

## Specifying your Webex token

The script requires an API token for sending messages. The safest way to specify your API token (or your bot's API token) is to set an environment variable. In MacOS:

```
export WEBEX_TOKEN=ZHF2YThmZTktY
```

In Windows:

```
set WEBEX_TOKEN=ZHF2YThmZTktY
```

It is also possible to specify the Webex token to be used at runtime using the `-t` option.

```
python webex-super-send.py -m FILE -l mylist.txt -t ZHF2YThmZTktY
```

## Extensions

| Extension | Description | Required? |
| :----- | :----- | :-----: |
| `-m` or `--message` | Specify the file that contains the message to be sent. | **YES** |
| `-l` | Specify the file that contains the recipients | no |
| `-t` or `--token` | Define the Webex API token to be used. Using environment variables is preferred. | no |
