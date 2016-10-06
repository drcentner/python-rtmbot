from __future__ import unicode_literals
# don't convert to ascii in py2.7 when creating string to return
from time import sleep

outputs = []


def xkcd_little_bobby_tables(data):
    # TODO: react to message with :troll:
    outputs.append([data['channel'], "https://www.xkcd.com/327/"])

def xkcd_microsoft_time(data):
    outputs.append([data['channel'], "5 minutes remaining..."])
    sleep(.5)
    outputs.append([data['channel'], "3 hours remaining..."])
    sleep(.5)
    outputs.append([data['channel'], "15 days remaining..."])
    sleep(.5)
    outputs.append([data['channel'], "7 seconds remaining..."])
    sleep(.5)
    outputs.append([data['channel'], "20 years remaining..."])
    sleep(.5)
    outputs.append([data['channel'], "https://xkcd.com/612/"])

def process_message(data):
    if 'little bobby tables' in data['text']:
        xkcd_little_bobby_tables(data)
    elif 'microsoft time' in data['text']:
        xkcd_microsoft_time(data)
