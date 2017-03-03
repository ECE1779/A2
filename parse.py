from edit_img import *
from search_img import *
from app import *


global requested_img_id 
requested_img_id = ""
global origin_url 
origin_url = ""
global offset
offset = 0
global command_dict 
command_dict = {}

def msg_handler(sender_id, message_text):
    global requested_img_id 
    global origin_url 
    global offset
    global command_dict 


    parsed_command = message_text.split(" ")
    print(parsed_command[0])
    
    if parsed_command[0] == ":select" :
        
        print("entered select")

        requested_img_id = upload_image(origin_url)        
        print("img selected " + str(requested_img_id))
    elif parsed_command[0] == ":edit":
        #TODO handle edit commands here
        print("entered edit")
        if parsed_command[1] == "height":
            if parsed_command[2].isdigit():
                if int(parsed_command[2]) > 0 and int(parsed_command[2]) <= 100:              

                    command_dict.update({"height":parsed_command[2]+"%"})
            else:
                send_message(sender_id, "input should be between 1 and 100")
            
        elif parsed_command[1] == "width":
            if parsed_command[2].isdigit():
                if int(parsed_command[2]) > 0 and int(parsed_command[2]) <= 100:              

                    command_dict.update({"width":parsed_command[2]+"%"})
                    
            else:
                send_message(sender_id, "input should be between 1 and 100")
            
        elif parsed_command[1] == "grayscale":
            

            command_dict.update({"grayscale":""})
        
        elif parsed_command[1] == "blur":
            

            command_dict.update({"blur":parsed_command[2]})

        else:
            send_message(sender_id, "wrong edit command!")

        #fucking send the command to image api
        print("img id " + str(requested_img_id))
        edited_img_url = get_image(str(requested_img_id), command_dict)
        send_image(sender_id, edited_img_url )

    elif parsed_command[0] == ":del":
        #TODO handle edit commands here
        print("entered del")
        if parsed_command[1] == "height":


            del command_dict["height"]

            
        elif parsed_command[1] == "width":

            del command_dict["width"]
        elif parsed_command[1] == "grayscale":

            del command_dict["grayscale"]
        
        elif parsed_command[1] == "blur":

            del command_dict["blur"]
        else:
            send_message(sender_id, "wrong edit command!")

        #fucking send the command to image api
        editted_img_url = get_image(requested_img_id, command_dict)
        send_image(sender_id, eddited_img_url)

    elif parsed_command[0] == ":next":
        # increment offset by 1
        print("entered next")
        offset += 1

        send_back(sender_id, message_text)

    elif parsed_command[0] == ":back":
        print("entered back")
        if offset == 0:
            send_back(sender_id, message_text)
        else:
            offset -= 1
            send_back(sender_id, message_text)
    else:
        # search the image 
        print("search img")
        offset = 0

        command_dict = dict()

        send_back(sender_id, message_text)


def send_back(sender_id, message_text):
    
    global origin_url
    
    result = search_image_3(message_text, offset)
    if result is None:
        send_message(sender_id, "Your image of " + message_text + " cannot be found.")
    else:
        send_message(sender_id, "Here's your picture of "+ message_text)
        origin_url = result
        print("set origin_url to " + origin_url)
        send_image(sender_id, result)



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
    print(str(message))
    sys.stdout.flush()





