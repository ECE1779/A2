import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "The service is up", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    if message_text == "trump":
                        send_message(sender_id, "make america great again")
                        result = search_image("donald trump", 0)
                        send_image(sender_id, result)
                    elif message_text == "hello":
                        send_message(sender_id, "world")
                    else:
                        send_message(sender_id, "here's your picture of "+ message_text)
                        result = search_image(message_text, 0)
                        send_image(sender_id, result)
                        
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200




########### Bing Search ############
########### Python 2.7 #############
#import http.client, urllib.request, urllib.parse, urllib.error, base64
import httplib, urllib, base64, json

def search_image(q, offset):


 
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'b23854bc1dc24ebcb32a94577b19b1c6',
    }

    params = urllib.urlencode({
        # Request parameters
        'q': q,
        'count': '1',
        'offset': offset,
        'mkt': 'en-us',
        'safeSearch': 'Off',
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    json_data = json.loads(data)
    #print(json_data)
    return json_data["value"][0]["contentUrl"]

####################################


def send_image(recipient_id, contentUrl):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=contentUrl))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
            "type":"image",
            "payload":{
            "url":contentUrl
      }
    }
  }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)



def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
