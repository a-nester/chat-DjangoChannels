from channels import Group
from .models import Message, Rooms
from django.contrib.auth.models import User
import json
import datetime

def ws_connect(message, room_pk):
    messages = Message.objects.filter(room = int(room_pk))
    dictionary = [i.format_response() for i in messages]
    Group('chat-%s' % room_pk).add(message.reply_channel)
    message.reply_channel.send({"accept": True})
    Group('chat-%s' % room_pk).send(
        {
            "text" : json.dumps({
                "preload" if len(dictionary) > 0 else "nomessage" : json.dumps(dictionary[10:] if len(dictionary) > 10 else dictionary)
            })
        }
    )

def ws_receive(message, room_pk):
    response = json.loads(message['text'])
    notice = None
    
    if 'newmessage' in response:
        data = response['newmessage']
        room = Rooms.objects.get(pk = int(data['room']))
        user = User.objects.get(username = data['username'])
        obj = Message(room = room, user = user, message = data['message'],
                    date = datetime.datetime.now())
        obj.save()
        room.users.remove(user)
        notice = obj.format_response()
    if 'writing' in response:
        data = response['writing']
        user = User.objects.get(username = data['username'])
        room = Rooms.objects.get(pk = int(data['room']))
        usernames = None
        if data['isSend'] == True:   
            room.users.add(user)
            usernames = [{ 'name' : us.username } for us in room.users.all()]            
        elif data['isSend'] == False:
            room.users.remove(user)
            usernames = [{ 'name' : us.username } for us in room.users.all()]
        notice = {
                'username' : str(user),
                'isSend' : True,
                'users' : usernames
        }  
    if type(notice) != None:
        Group('chat-%s' % room_pk).send(
            {
                "text" : json.dumps({
                    "newmessage" : json.dumps(notice)
                })
            }
        )
    
def ws_disconnect(message, room_pk):
    Group('chat-%s' % room_pk).discard(message.reply_channel)
