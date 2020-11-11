from eliza.eliza import Eliza
from fbchat import Client
from fbchat.models import *
import json

with open("creds.json", 'r') as f:
    creds = json.load(f)
    email = creds["email"]
    passw = creds["passw"]

print('email:',email)
print('password:',passw)

cookies = ""
try:
    # Load the session cookies
    with open('session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    pass

eliza = Eliza()
eliza.load('eliza\doctor.txt')

users = [];

class CustomClient(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        print("Thread type:",ThreadType.USER)
        if(thread_type!=ThreadType.USER):
            return;
        if(author_id!=thread_id):
            return;
        print('Recieved msg:',msg);
        print('\n\n\nRecieved Message:',msg["body"]);
        reply = ""
        if(author_id in users):
            reply = eliza.respond(msg["body"])
        else:
            users.append(author_id)
            reply = eliza.initial()
        if reply is None:
            return;
        print("Replying:",reply)
        client.sendMessage(reply,thread_id,thread_type)

        pass







# Attempt a login with the session, and if it fails, just use the email & password
client = CustomClient(email,passw, session_cookies=cookies)
client.listen()

# ... Do stuff with the client here






# Save the session again
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)







if not client.isLoggedIn():
    client.login(email, passw)

session_cookies = client.getSession()
client.setSession(session_cookies)