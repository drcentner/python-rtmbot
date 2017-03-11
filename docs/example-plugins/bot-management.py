from __future__ import unicode_literals
# don't convert to ascii in py2.7 when creating string to return
import yaml
from client import slack_client as sc

# Import variables from config file
config = yaml.load(open('plugins/bot-management.conf', 'r'))

bot_message_delete_reactions = config.get('BOT_MESSAGE_DELETE_REACTIONS')
# user permission requirement not yet implemented
bot_message_delete_auth_users = config.get('BOT_MESSAGE_DELETE_AUTH_USERS')

def bot_message_delete(data):
    if data['reaction'] in bot_message_delete_reactions:# and data['user'] in bot_message_delete_auth_users:
        response = sc.api_call(
            'chat.delete',
            ts=data['item']['ts'],
            channel=data['item']['channel']
            )

def process_reaction_added(data):
    try:
        bot_message_delete(data)
    except:
        pass
