from __future__ import unicode_literals
# don't convert to ascii in py2.7 when creating string to return
import yaml
import re

# Import variables from config file
config = yaml.load(open('plugins/servicenow.conf', 'r'))

instance = config.get('SERVICENOW_INSTANCE')
search_regex = config.get('SERVICENOW_SEARCH_REGEX')

outputs = []


def process_message(data):
    # Search the message text for patterns indicative of a ServiceNow ticket
    ticket_search = re.search(search_regex, data['text'], re.IGNORECASE)

    # If a matching pattern was found
    if ticket_search:
        # Format the SN search URL using the instance variable
        ticket_url = 'https://' + instance + '.service-now.com/nav_to.do?uri=textsearch.do?sysparm_search=' + ticket_search.group()

        # Output the URL
        outputs.append([data['channel'], ticket_url])
