from eliza.eliza import Eliza
from fbchat import Client,TypingStatus
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
    def onCallStarted(mid, caller_id, is_video_call, thread_id, thread_type, ts, metadata, msg):
        client.sendMessage("Stop calling you cunt!",thread_id,thread_type)




    global lastSent
    global lastSauce
    lastSent = lastSauce = ""
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        global lastSent
        global lastSauce

        senderInfo = client.fetchUserInfo(author_id).get(author_id)
        senderName = senderInfo.first_name

        if message_object.text is None:
            print("no body found in message!")
            return
        if "hahaha" in message_object.text.lower():
            client.reactToMessage(mid, MessageReaction.SMILE)

            
        if thread_type!=ThreadType.USER and "eliza" not in message_object.text.lower():
            print("group detected")
            if message_object.replied_to is None:
                return
            elif message_object.replied_to.author != self.uid:
                return

        message_object.text = message_object.text.lower().replace('eliza','')


        message_object.text = message_object.text.lower().replace('eliza','')
        text = message_object.text;


        if(author_id==self.uid):
            return
        
        print('\n\n\nRecieved Message:',text," from:",senderInfo.name);
        reply = ""

        if "love" in text:
            client.reactToMessage(mid, MessageReaction.LOVE)
        if "wow" in text:
            client.reactToMessage(mid, MessageReaction.WOW)
        if "grr" in text:
            client.reactToMessage(mid, MessageReaction.ANGRY)
        if "give sauce" in text or "give source" in text:
            reply = lastSauce    
        elif "remove that shit" in text:
            client.unsend(lastSent)
        elif "commit sudoku" in text:
            exit()
        
        elif "fuck you bitch" in text:
            user = client.fetchUserInfo(author_id)
            print(user)
            reply = "🖕"
            # Client.reactToMessage(Client, mid,MessageReaction.ANGRY);
        elif "show me" in text:
            q = text.split("show me")[1]
            q = remove_control_characters(q).replace(" ", "+")
            url = google.randomImgSearch(q)
            if url == -1:
                reply = "Sorry, "+senderName+" but I am not able to send Images at the moment :( !"
            elif url is None:
                print('no image found')
                reply = "Nothing found boss!"
            else:
                lastSauce = url;
                lastSent = sendImg(url,thread_id, thread_type)
            
        else:
            reply = eliza.respond(text)

        if reply is None:
            return;

        print("Replying:",reply)
        lastSent = client.send(Message(text=reply,reply_to_id=mid),thread_id,thread_type)
        


# Attempt a login with the session, and if it fails, just use the email & password
client = CustomClient(email,passw, session_cookies=cookies)
lastSent = lastSauce = ""
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
