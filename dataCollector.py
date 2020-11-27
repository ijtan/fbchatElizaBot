import csv
import os

csvfile = "messages.csv" #add file integration

def getMessage(message_id):
    with open('items.csv', 'r'):
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            if row.get('mid') is not None and row.get('mid') == message_id:
                return row
        

def addMessage(threadID, message_object):
    with open("messages.csv", "a", newline="") as f:
        keys = ["thread","author", "replied_to", "text","mid","timestamp"]

        writer = csv.writer(f, quoting=csv.QUOTE_NONE, quotechar='',  lineterminator='\n',escapechar='\\')
        
        if os.path.getsize("messages.csv") == 0:
            writer.writerow(keys)
        if message_object.replied_to is None:
            repl = "-"
        else:
            repl = message_object.replied_to.uid

    
        message = [threadID, message_object.author,repl, message_object.text, message_object.uid,message_object.timestamp]
        writer.writerow([str(row) for row in message])


def getStatistics():
    #get all entries form the csv
    #group entried by thread
    #iterate though all messages, and increment count per user
        #so like if user exists -> count['user']++
        #else add user -> count['user']++
    #finally convert ids into names using fetch details 
    #format pretty into a like leader board with    
    #Top X biggests losers:
    #1st Loser | Name: | Message-Count:
    #...

    pass

# def addReact(react, message_id)