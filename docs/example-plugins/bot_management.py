from __future__ import unicode_literals
# don't convert to ascii in py2.7 when creating string to return
import yaml
import requests
from client import slack_client as sc

# Import variables from config file
config = yaml.load(open('plugins/bot_management.conf', 'r'))

bot_message_delete_reactions = config.get('BOT_MESSAGE_DELETE_REACTIONS')
bot_message_delete_auth_usernames = config.get('BOT_MESSAGE_DELETE_AUTH_USERS')
bot_message_delete_auth_group_handles = config.get('BOT_MESSAGE_DELETE_AUTH_GROUPS')
url_usergroups_list = config.get('URL_USERGROUPS_LIST')



outputs = []



def is_user_authorized(userid, username, usernames, group_handles):
    try:
        usernames_len = len(usernames)
    except:
        usernames_len = 0

    try:
        group_handles_len = len(group_handles)
    except:
        group_handles_len = 0

    if usernames_len > 0 and username in usernames:
        return True
    elif group_handles_len > 0:
        # Cannot utilize sc.api_call here because bots are not allowed to use usergroups.list
        #usergroups = sc.api_call('usergroups.list',include_users=True)

        # Workaround to allow a bot to access usergroup information
        r = requests.get(url_usergroups_list, timeout=10)
        usergroups = r.json()

        for usergroup in usergroups['usergroups']:
            if usergroup['handle'] in group_handles and userid in usergroup['users']:
                return True
    else:
        return False

    # If we got this far, user is not authorized
    return False

def get_username_from_id(userid):
    users = sc.api_call('users.list')

    for user in users['members']:
        if user['id'] == userid:
            return user['name']

    return False

def bot_message_delete(data):
    userid = data['user']

    try:
        username = get_username_from_id(userid)
    except:
        outputs.append([data['item']['channel'], "Failed to get username for user ID: {0}".format(userid)])
        return False

    user_is_authorized = is_user_authorized(userid, username, bot_message_delete_auth_usernames, bot_message_delete_auth_group_handles)

    if data['reaction'] in bot_message_delete_reactions and user_is_authorized:
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
