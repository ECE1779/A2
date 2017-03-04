from edit_img import *
from search_img import *
from send import *
from myds import *



def msg_handler(sender_id, message_text, newsearch):
    #global newsearch

    parsed_command = message_text.split(" ")
    #print(parsed_command[0])
    
    if parsed_command[0] == ":select" :
        
        print("entered select")
        newsearch.select()        
        print("img selected " + str(newsearch.requested_img_id))
    elif parsed_command[0] == ":edit":
        #TODO handle edit commands here
        print("entered edit")
        if parsed_command[1] == "height" or parsed_command[1] == "width":
            if parsed_command[2].isdigit():
                if int(parsed_command[2]) > 0 and int(parsed_command[2]) <= 100:              
                    print("send command %s %s" % parsed_command[1], parsed_command[2])
                    newsearch.edit(parsed_command)
                    print("new commands" + newsearch.command_dict)
            else:
                send_message(sender_id, "input should be between 1 and 100")
            
                    
        elif parsed_command[1] == "grayscale" or parsed_command[1] == "blur":

            print("send command " + parsed_command[1])
            newsearch.edit(parsed_command)
            print("new commands" + newsearch.command_dict)
            
        else:
            send_message(sender_id, "wrong edit command!")

        #fucking send the command to image api
        print("sending img to edit " + str(newsearch.requested_img_id))
        editted_img_url = get_image(str(newsearch.requested_img_id), newsearch.command_dict)
        print("editted url " + editted_img_url)
        send_image(sender_id, editted_img_url )

    elif parsed_command[0] == ":del":
        #TODO handle edit commands here
        print("entered del")
        if parsed_command[1] == "height" or parsed_command[1] == "width" or parsed_command[1] == "grayscale" or parsed_command[1] == "blur":


            newsearch.delete(parsed_command)
            print("deleted command" + parsed_command[1])
        else:
            send_message(sender_id, "wrong edit command!")

        #fucking send the command to image api
        print("sending img to edit " + str(newsearch.requested_img_id))
        editted_img_url = get_image(str(newsearch.requested_img_id), newsearch.command_dict)
        print("editted url " + editted_img_url)
        send_image(sender_id, editted_img_url )

    elif parsed_command[0] == ":next":
        # increment offset by 1
        print("entered next")
        newsearch.next_img()
        result = search_image_3(message_text, newsearch.offset)
        if result is None:
            send_message(sender_id, "Your image of " + message_text + " cannot be found.")
        else:
            send_message(sender_id, "Here's your picture of "+ message_text)
            newsearch.origin_url = result
            print("set origin_url to " + newsearch.origin_url)
            send_image(sender_id, result)

    elif parsed_command[0] == ":back":
        print("entered back")
        newsearch.prev_img()
        result = search_image_3(message_text, newsearch.offset)

        send_message(sender_id, "Here's your picture of "+ message_text)
        newsearch.origin_url = result
        print("set origin_url to " + newsearch.origin_url)
        send_image(sender_id, result)

    else:
        # search the FUCKING IMAGE 
        print("search img")
        result = search_image_3(message_text, newsearch.offset)
        if result is None:
            send_message(sender_id, "Your image of " + message_text + " cannot be found.")
        else:
            send_message(sender_id, "Here's your picture of "+ message_text)
            newsearch = searchinfo()
            
            newsearch.origin_url = result
            print("set origin_url to " + newsearch.origin_url)
            send_image(sender_id, result)











