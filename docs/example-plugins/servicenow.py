from __future__ import unicode_literals
# don't convert to ascii in py2.7 when creating string to return
from client import slack_client as sc
import yaml
import re

# Import variables from config file
config = yaml.load(open('plugins/servicenow.conf', 'r'))

instance = config.get('SERVICENOW_INSTANCE')
search_regex = config.get('SERVICENOW_SEARCH_REGEX')

outputs = []


# The RTM API sometimes processes the bot's last posted message
# upon connection. This can result in the bot posting duplicate URL's
# when it connects under certain circumstances (e.g. disconnect/reconnect).
# Also, there's probably few, if any, circumstances where the bot
# responding to messages it posted would be desired behavior.
bot_user_id = sc.api_call('auth.test')['user_id']

def process_message(data):
    # If the message was not posted by the Slack bot
    if data['user'] != bot_user_id:
        # Split message content up by whitespace
        strings = re.split('\s+', data['text'])

        # For each grouping of characters
        for string in strings:
            # Remove non-alphanumeric characters
            string = re.sub('\W+', '', string)

            # Search for a regex pattern match
            ticket = re.match(search_regex, string, re.IGNORECASE)

            # If a match was found
            if ticket:
                # Format the SN search URL using the instance variable
                ticket_url = 'https://' + instance + '.service-now.com/nav_to.do?uri=textsearch.do?sysparm_search=' + ticket.group()

                # Output the URL
                outputs.append([data['channel'], ticket_url])
