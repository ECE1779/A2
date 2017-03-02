requested_img_id = ""
origin_url = ""
offset = 0
command_dict = dict()

def msg_handler(sender_id, message_text):
    parsed_command = message_text.split(" ")
    if parsed_command[0] == ":select" and origin_url != "":
        
        requested_img_id = upload_image(origin_url)

    elif parsed_command[0] == ":edit":
        #TODO handle edit commands here
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
        editted_img_url = get_image(requested_img_id, command_dict)
        send_image(sender_id, eddited_img_url)

    elif parsed_command[0] == ":del":
        #TODO handle edit commands here
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
        offset += 1
        send_back(sender_id, message_text)

    elif parsed_command[0] == ":back":
        if offset == 0:
            send_back(sender_id, message_text)
        else:
            offset -= 1
            send_back(sender_id, message_text)
    else:
        # search the image 
        offset = 0
        command_dict = dict()

        send_back(sender_id, message_text)


def send_back(sender_id, message_text):
    result = search_image_3(message_text, offset)
    if result is None:
        send_message(sender_id, "Your image of " + message_text + " cannot be found.")
    else:
        send_message(sender_id, "Here's your picture of "+ message_text)
        origin_url = result
        send_image(sender_id, result)




