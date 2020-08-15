from typing import Dict, List
from twilio.twiml.messaging_response import MessagingResponse
from DB import DB

# Formats contacts to fix encoding issues
def formatContacts(contacts: Dict):
    for key in contacts:
        contacts[key] = contacts[key].strip().encode('ascii', 'ignore').decode('ascii', 'ignore')
    return contacts

# Store contacts and MessageResponse
class Communication:
    from os import environ
    from twilio.rest import Client
    client = Client(environ['TWILIO_ACCOUNT_SID'], environ['TWILIO_AUTH_TOKEN'])

    # Read in phone numbers from environment
    contacts : Dict = formatContacts({
        "Twilio" : environ.get("TWILIO"),
        "Param": environ.get("PARAM"),
        "Arjun": environ.get("ARJUN"),
        "Nishant": environ.get("NISHANT")
    })

    # Message which will be sent back to member
    resp : MessagingResponse = None

    @staticmethod
    def reply(text : str):
        Communication.resp = MessagingResponse()
        Communication.resp.message(text)

    @staticmethod
    def send(text : str, member_name : str):
        Communication.client.messages.create(
            from_ = Communication.contacts['Twilio'],
            to = Communication.contacts[member_name],
            body = text
        )

# Notifies members of their excessive balances
def alert(excessive: List[Dict]):
    for member in excessive:
        if member['Name'] in Communication.contacts:
            Communication.send("Your current balance is ${:.2f}".format(member['Balance']), member['Name'])

# Adds SMS order to database
def addSMSorder(body : List[str]):
    # Parse message into necessary attributes
    location = body[0].strip().title()
    subtotals : Dict[str, float] = dict()
    for i in range(1, len(body) - 1):
        parts = body[i].split(' ')
        member_name = parts[0].strip()
        # Checks if values associated with each member is a float or a mathematical expression
        if checkFloat(parts[1].strip()):
            subtotals[member_name] = float(parts[1].strip())
        else:
            from numexpr import evaluate
            subtotals[member_name] = evaluate(parts[1].strip())

    # Total cost of the order
    total : float = float(body[-1].strip())

    from Order import Order
    from datetime import datetime
    excessive : List[Dict] = DB.add(Order(datetime.now(), location, subtotals, total))

    # Sends member a confirmation message
    Communication.reply("\nAdded order from %s for a total of $%.2f" % (location, total))
    alert(excessive)

# Credits balance of given member in spreadsheet
def credit(name : str, value : float):
    new_balance : float = DB.credit(name, value)
    Communication.reply("Your new balance is ${:.2f}".format(new_balance))
    Communication.send("%s credited $%.2f to their balance" % (name, value), "Nishant")

# Check if given value is a float
def checkFloat(value : str) -> bool:
    value = value.replace(".", "", 1).strip()
    if value.isdigit():
        return True
    elif value[0] == "-" and value[1:].isdigit():
        return True
    return False

# Manages two-way communication
def sms():
    from flask import request
    # Reformats phone number of member
    phone = request.form['From'][:2] + " (" + request.form['From'][2:5] + ") " + request.form['From'][5:8] + "-" + request.form['From'][8:]

    # Split message line by line
    body : List[str] = request.form['Body'].split('\n')
    for i in range(len(body)):
        body[i] = body[i].strip()

    # Store command string
    command : str = body[0].title()

    if command == "Credit":
        # If credit message is correctly formatted
        if checkFloat(body[1]):
            # Search for phone number corresponding to member
            for key in Communication.contacts:
                if Communication.contacts[key] == phone:
                    # Credit balance of member who messaged
                    credit(key, float(body[1]))
        else:
            Communication.reply("The first line of your message must be 'Credit/credit' and "
                         "the second line must be a number indicating how much you would like to credit your balance by")
    else:
        # Restricts add authorization to phone number corresponding to Nishant
        if phone == Communication.contacts['Nishant']:
            # Adds order to spreadsheet
            addSMSorder(body)
        else:
            Communication.reply("You only have permission to credit your balance")

    return str(Communication.resp)