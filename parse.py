from edit_img import *
from search_img import *
from send import *
from myds import *



def msg_handler(newsearch):


    parsed_command = newsearch.topic.split(" ")
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

                    newsearch.edit(parsed_command)
            else:
                send_message(newsearch.sender_id, "input should be between 1 and 100")
            
                    
        elif parsed_command[1] == "grayscale":
            

            newsearch.edit(parsed_command)
        
        elif parsed_command[1] == "blur":
            

            newsearch.edit(parsed_command)

        else:
            send_message(newsearch.sender_id, "wrong edit command!")

        #fucking send the command to image api
        print("img id " + str(newsearch.requested_img_id))
        edited_img_url = get_image(str(requested_img_id), newsearch.command_dict)
        send_image(newsearch.sender_id, edited_img_url )

    elif parsed_command[0] == ":del":
        #TODO handle edit commands here
        print("entered del")
        if parsed_command[1] == "height" or parsed_command[1] == "width" or parsed_command[1] == "grayscale" or parsed_command[1] == "blur":


            newsearch.delete(parsed_command)

        else:
            send_message(sender_id, "wrong edit command!")

        #fucking send the command to image api
        editted_img_url = get_image(requested_img_id, command_dict)
        send_image(sender_id, eddited_img_url)

    elif parsed_command[0] == ":next":
        # increment offset by 1
        print("entered next")
        newsearch.next_img()
        result = search_image_3(newsearch.topic, newsearch.offset)
        if result is None:
            send_message(newsearch.sender_id, "Your image of " + newsearch.topic + " cannot be found.")
        else:
            send_message(newsearch.sender_id, "Here's your picture of "+ newsearch.topic)
            newsearch.origin_url = result
            print("set origin_url to " + newsearch.origin_url)
            send_image(newsearch.sender_id, result)

    elif parsed_command[0] == ":back":
        print("entered back")
        newsearch.prev_img()
        result = search_image_3(newsearch.topic, newsearch.offset)

        send_message(newsearch.sender_id, "Here's your picture of "+ newsearch.topic)
        newsearch.origin_url = result
        print("set origin_url to " + newsearch.origin_url)
        send_image(newsearch.sender_id, result)

    else:
        # search the image 
        print("search img")
        
        newsearch.offset = 0
        newsearch.command_dict = {}

        result = search_image_3(newsearch.topic, newsearch.offset)
        if result is None:
            send_message(newsearch.sender_id, "Your image of " + newsearch.topic + " cannot be found.")
        else:
            send_message(newsearch.sender_id, "Here's your picture of "+ newsearch.topic)
            newsearch.origin_url = result
            print("set origin_url to " + newsearch.origin_url)
            send_image(newsearch.sender_id, result)











