import os
import sys
import json

import requests
from flask import Flask, request
from parse import *
from send import *
from myds import *

app = Flask(__name__)
newsearch = searchinfo()
print("global newsearch set")

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
                    if message_text == ":?":
                        help = """Type keywords to search images.\n \
                                Add edit commands after your keyworkds to edit the image, separate by :\n\
                                Supported commands:\n\
                                height [num]%\n\
                                width [num]%\n\
                                blur [num]\n\
                                grayscale\n\
                                example: catfish: height 80%: width 80%: blur 5: grayscale
                                """
                        sender_message(sender_id,help)
                        return
                    global newsearch
                    #newsearch = searchinfo()
                    newsearch = msg_handler(sender_id, message_text, newsearch)                    
                    #msg_handler(newsearch)
                    """
                    result = search_image_3(message_text, 0)
                    if result is None:
                        send_message(sender_id, "Your image of " + message_text + " cannot be found.")
                    else:
                        send_message(sender_id, "Here's your picture of "+ message_text)
                        send_image(sender_id, result)
                    """
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200








def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    
    app.run(debug=True)
