from eliza.eliza import Eliza
from fbchat import Client,TypingStatus
from fbchat.models import *
import json
import google
import unicodedata
import os

with open("creds.json", 'r') as f:
    creds = json.load(f)
    email = creds["email"]
    passw = creds["passw"]

print('email:',email)
lng = len(passw)
passw = passw[:2]
for x in range(2,lng):
    passw+='*'
print('password:',passw)

blacklist = open("blacklist.txt",'r').read()
blacklist.split('\n')

cookies = ""
with open('session.json', 'r') as f:
    cookies = json.load(f)

bookmarks = {}
if os.path.exists('bookmarks.json'):
    with open('bookmarks.json', 'r') as f:
        try:
            bookmarks = json.load(f)
        except:
            print("Failed to load bookmarks!")
else:    
    with open('bookmarks.json', 'w') as f:        
            json.dump(bookmarks, f)
        
        


eliza = Eliza()
eliza.load('eliza/doctor.txt')

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")


def updateBookmarks():
    with open('bookmarks.json', 'w') as f:  
        json.dump(bookmarks, f)


class CustomClient(Client):
    def onCallStarted(mid, caller_id, is_video_call, thread_id, thread_type, ts, metadata, msg):
        client.sendMessage("Stop calling grr!",thread_id,thread_type)

    

    global bookmarks
    global lastSent
    global lastSauce
    lastSent = lastSauce = ""
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        global lastSent
        global lastSauce
        done = False
        reply = ""

        senderInfo = client.fetchUserInfo(author_id).get(author_id)
        senderName = senderInfo.first_name

        if author_id == self.uid or author_id in blacklist:
            return

        if message_object.text is None:
            print("no body found in message!")
            return


        if self.uid == author_id:
            return
        


        text = message_object.text.lower()
        
        if "hahaha" in text or "bhahha" in text or "funny" in text:
            client.reactToMessage(mid, MessageReaction.SMILE)
        if "love" in text or "xxxx" in text:
            client.reactToMessage(mid, MessageReaction.LOVE)
        if "wow" in text:
            client.reactToMessage(mid, MessageReaction.WOW)
        if "grr" in text or "angry" in text:
            client.reactToMessage(mid, MessageReaction.ANGRY)
        if "sad" in text:
            client.reactToMessage(mid, MessageReaction.SAD)

        if thread_type!=ThreadType.USER and "eliza" not in message_object.text.lower():
            if message_object.replied_to is None:
                return
            elif message_object.replied_to.author != self.uid:
                return

        message_object.text = message_object.text.lower().replace('eliza','')
        text = message_object.text;


        
        
        print('\n\n\nRecieved Message:',text," from:",senderInfo.name);
        
        
        if done:
            pass
        elif "@everyone" in text:
            # if thread_type != ThreadType.GROUP:
            #     return
            # group = client.fetchGroupInfo(thread_id)[thread_id]
            # mentions = [Mention(uid, 0, len("@everyone")) for uid in group.participants]
            # print("Mentions: ",mentions)
            # lastSent = client.send(Message(text="@everyone", mentions=mentions), thread_id=thread_id, thread_type=thread_type)
            group = client.fetchThreadInfo(thread_id)[thread_id]
            author = self.fetchUserInfo(author_id)[author_id].name
            # logger.info('@everyone in '+str(group.name)+" by: "+author)
            mentions = []
            text = "@everyone: "
            for i in group.participants:
                usertag = "@"+self.fetchUserInfo(i)[i].name
                mstart = len(text)
                text += usertag+ " / "
                mlen = len(usertag)

                mentions.append(Mention(str(i), offset=mstart, length=mlen))
            text = text[:-3]
            lastSent = self.send(Message(text=text, mentions=mentions), thread_id=thread_id, thread_type=thread_type)
            return
        elif "give sauce" in text or "give source" in text:
            reply = lastSauce   



        elif "new bookmark" in text or "add bookmark" in text:
            if bookmarks.get(thread_id) is None:
                bookmarks[thread_id] = {}

            if message_object.replied_to is None:
                reply = "bookmark does not reply to anything"
                
            else:    
                bmID = message_object.replied_to.uid
                bmKey = text.split("bookmark")[1]
                # bmText = message_object.replied_to.text.lower()
                bookmarks[thread_id][bmKey] = bmID
                reply = "added new bookmark!"  
            updateBookmarks()


        elif "get bookmarks" in text or "get all bookmarks" in text:
            if bookmarks.get(thread_id) is None:
                bookmarks[thread_id] = {}

            keys = bookmarks[thread_id].keys()
            if(len(keys)==0):
                reply = "no bookmarks found!"
            else:
                i = 1
                for k in keys:
                    reply+=f": {k}\n"
                    i+=1


        elif "get bookmark" in text:

            bmID = text.split("bookmark")[1]

            if bookmarks.get(thread_id) is None:
                bookmarks[thread_id] = {}

            if bookmarks[thread_id].get(bmID) is not None:
                mid = bookmarks[thread_id].get(bmID)
                reply = '.'
            else:
                reply = "Could not find bookmark"

        elif "remove bookmark" in text or "delete bookmark" in text:

            bmID = text.split("bookmark")[1]

            if bookmarks.get(thread_id) is None:
                bookmarks[thread_id] = {}

            if bookmarks[thread_id][bmID] is not None:
                del bookmarks[thread_id][bmID]
                reply = 'Deleted Bookmark!'
            else:
                reply = "Could not find bookmark"
            updateBookmarks()




        elif "remove that" in text or "delete that" in text:
            if message_object.replied_to is None:
                client.unsend(lastSent)
                return
            else:
                client.unsend(message_object.replied_to.uid)
                return

        # elif "commit sudoku!" in text:
        #     exit()
        
        elif "fuck you" in text:
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
