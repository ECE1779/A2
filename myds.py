
import os
import sys
import json

import requests
from flask import Flask, request
from parse import *
from send import *
from myds import *
from edit_img import *



def upload_image(url):
    # https://api.imageresizer.io/images?key=8306ec405392ace375c33449ab79acbdcea54890&url=https://upload.wikimedia.org/wikipedia/commons/6/65/Tesla_Model_S_Indoors.jpg
    # this should return an image url
    params = urllib.parse.urlencode({
        'key': '8306ec405392ace375c33449ab79acbdcea54890',
        'url': url,
    })

    try:
        conn = http.client.HTTPSConnection('api.imageresizer.io')
        conn.request("GET", "/images?%s" % params)
        response = conn.getresponse()

        data = response.read()
        json_data = json.loads(data)
        while json_data["success"] == False:
            response = conn.getresponse()
            data = response.read()
            json_data = json.loads(data)
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    
    #print(json_data)

    if json_data["success"] == False:
        return None
    else:
        return json_data["response"]["id"]

def get_image(img_id, command):
    head = "https://im.ages.io/"
    print(img_id)
    #img_id
    #"?"
    params = urllib.parse.urlencode(command)

    img_url = head + img_id + "?" + params
    return img_url

class searchinfo(object):

    def __init__(self, sender_id, topic):
        self.sender_id = sender_id
        self.topic = topic
        self.requested_img_id = ""
        self.origin_url = ""
        self.offset = 0
        self.command_dict = {}
        
    def select(self):
        self.requested_img_id = upload_image(self.origin_url)
        
    def edit(self, parsed_command):
        self.command_dict.update({parsed_command[1]:parsed_command[2]})
        
    def delete(self, parsed_command):
        del self.command_dict[parsed_command[1]]
        
    def next_img(self):
        self.offset += 1
        self.origin_url = search_image_3(self.topic, self.offset)
        
    def prev_img(self):
        if self.offset > 0:
            self.offset -=1
        self.origin_url = search_image_3(self.topic, self.offset)
    
