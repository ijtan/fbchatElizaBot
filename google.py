import os
import json
import random
import imghdr
import sys
import urllib.request
import urllib.parse
with open("creds.json", 'r') as f:
    creds = json.load(f)
    api = creds["api"]
    sid = creds["sid"]

API_KEY = api  # put your API key here
SEARCH_ENGINE_ID = sid  # you also have to generate a search engine token

def randomImgSearch(q,oldURL=None):
    for arg in sys.argv[1:]:
        q += urllib.parse.quote(arg) + '+'

    request = urllib.request.Request(
        'https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' +
        SEARCH_ENGINE_ID + '&q=' + q + '&searchType=image')

    data = ""
    try:
        with urllib.request.urlopen(request) as f:
            data = f.read().decode('utf-8')
    except: 
        print("API OVERLOADED")
        return -1
        
    data = json.loads(data)
    # print(data)
    if data.get('items') is None:
        return None
    results = data['items']
    url = random.choice(results)['link']
    
    # return (url)

    if oldURL is not None and url==oldURL:
        return None

    data = urllib.request.urlopen(url).read()

    imagetype = imghdr.what(None,data)
    if imagetype is None or imagetype=='':
        print("bad image found... Rerunning")

        newURL = randomImgSearch(q,url)
        # os.remove(data)
        return newURL
    # os.remove(data)
    print('found image of type:',imagetype)
    return url
# if not type(imagetype) is None:
#     os.rename('./image', './image.' + imagetype)
