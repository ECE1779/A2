import httplib, urllib,  base64, json
import os
import sys
import json

import requests


########### ImageResizer ###########
def upload_image(url):
    # https://api.imageresizer.io/images?key=key&url=https://upload.wikimedia.org/wikipedia/commons/6/65/Tesla_Model_S_Indoors.jpg
    # this should return an image url
    params = urllib.urlencode({
        'key':  os.environ["IMG_RESIZER_TOKEN"],
        'url': url,
    })
    #print("uploading image url is "+url)
    try:
        conn = httplib.HTTPSConnection('api.imageresizer.io')
        conn.request("GET", "/images?%s" % params)
        response = conn.getresponse()
        #print(response)
        data = response.read()
        #print(data)
        json_data = json.loads(data)
        
        #while json_data["success"] == False:
        #    response = conn.getresponse()
        #    data = response.read()
        #    json_data = json.loads(data)
        
        #print(data)
        conn.close()
    except Exception as e:
        print("error uploading img")
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))

    
    #print(json_data)

    if json_data["success"] == False:
        return None
    else:
        return json_data["response"]["id"]

def get_image(img_id, command):
    head = "https://im.ages.io/"
    
    #img_id
    #"?"
    params = urllib.urlencode(command)

    img_url = head + img_id + "?" + params
    return img_url



####################################
