from __future__ import print_function
import os
import sys
import json
import requests
from parse import *
from send import *

print('Loading function')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print('got new request')
    if 'params' in event :
        #print(event['params']['querystring']['hub.verify_token'])
        if 'querystring' in event['params']:

            if 'hub.verify_token' in event['params']['querystring']:
                verify_token = event['params']['querystring']['hub.verify_token']
                print("verify token is " + verify_token)
                
            if verify_token == os.environ["VERIFY_TOKEN"]:
                print("verification success")
                return int(event['params']['querystring']["hub.challenge"])
                
                
    #echo back messages
    if event["object"] == "page":

        for entry in event["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    
                    #send_message(sender_id,"Hello World! " + message_text)
                    if message_text == ":?":
                        help_msg = """Type keywords to search images.\nAdd edit commands after your keyworkds to edit the image, separate by :\nsupported commands:\nheight [num]%\nwidth [num]%\nblur [num]\ngrayscale\nellipse\n\nps: using only one of height and width can only scale the image,\nif you want to crop the image please use both of them"""
                        
                        send_message(sender_id,help_msg)
                        send_message(sender_id, "pps: ellipse cannot be used with grayscale and blur at the same time if the image size is large")
                        send_message(sender_id, "Use the following example to get started!")
                        send_message(sender_id, "catfish: height 30%: width 30%: blur 5: grayscale: ellipse")
                        return "ok", 200
                    
                    msg_handler(sender_id, message_text) 
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200
    #raise Exception('Something went wrong')



        
