from eliza.eliza import Eliza
from fbchat import Client
from fbchat.models import *
import json
import google
import unicodedata

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
eliza.load('eliza/doctor.txt')

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")



class CustomClient(Client):
    global lastSent
    lastSent = ""
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        global lastSent
        if(thread_type!=ThreadType.USER):
            if("eliza" not in msg["body"].lower()):
                return;
            else:
                msg["body"] = msg["body"].lower().replace('eliza','')
        if(author_id==self.uid):
            return;
        # print('Recieved msg:',msg);
        print('\n\n\nRecieved Message:',msg["body"]);
        reply = ""
            # if("love you" in msg["body"].lower()):
                # Client.reactToMessage(Client, mid,MessageReaction.LOVE);           
                
        if("remove that shit" in msg["body"].lower()):
            client.unsend(lastSent)
        elif("commit sudoku" in msg["body"].lower()):
            exit()
        
        elif("fuck you bitch" in msg["body"].lower()):
            reply = "🖕"
            # Client.reactToMessage(Client, mid,MessageReaction.ANGRY);
        elif("show me" in msg["body"].lower()):
            q = msg["body"].lower().split("show me")[1]
            q = remove_control_characters(q).replace(" ", "+")
            url = google.randomImgSearch(q)
            if url is None:
                print('no image found')
                reply = "Nothing found boss!"
            else:
                lastSent = sendImg(url,thread_id, thread_type)
            
        else:
            reply = eliza.respond(msg["body"])

        if reply is None:
            return;

        print("Replying:",reply)
        lastSent = client.sendMessage(reply,thread_id,thread_type)


# Attempt a login with the session, and if it fails, just use the email & password
client = CustomClient(email,passw, session_cookies=cookies)
lastSent = ""
def sendImg(url,tid,tt):
    print("image url",url)
    return client.sendRemoteFiles(url,Message(),tid,tt)
# def unSendMsg(mid):
#     client.unsend(mid)


client.listen()


# Save the session again
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)


if not client.isLoggedIn():
    client.login(email, passw)

session_cookies = client.getSession()
client.setSession(session_cookies)
