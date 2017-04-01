from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from api.models import Account
#
#TODO
# 1. A User follows you
# 2. Another User replies to your civi
# 3. civi was added to a civi that you've contributed to

# Live: User is in thread:
# 1. Another User makes a civi
# 2. Another User replies to your civi
# 3. A Civi is Modified
# 4. A Civi is Deleted



# Connected to websocket.connect
@channel_session
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("chat-%s" % room).add(message.reply_channel)

# Connected to websocket.receive
@channel_session
def ws_message(message):
    Group("chat-%s" % message.channel_session['room']).send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)

@channel_session_user_from_http
def thread_connect(message, thread_id):
    Group("thread-%s" % thread_id).add(message.reply_channel)
    # Accept the connection request
    message.reply_channel.send({"accept": True})

@channel_session_user
def thread_message(message, thread_id):
    # username = Account.objects.get(user=message.user.id)
    username = message.user.username
    Group("thread-%s" % thread_id).send({
        "text": "User " + str(username) + " says: " + message['text'],
    })
@channel_session
def thread_disconnect(message, thread_id):
    Group("thread-%s" % thread_id).discard(message.reply_channel)
