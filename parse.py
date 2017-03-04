from edit_img import *
from search_img import *
from send import *
from myds import *



def msg_handler(sender_id, message_text):
    
    parsed_command = message_text.split(":")
    #print(parsed_command[0])
    if len(parsed_command) > 5:
        send_message(sender_id, "Too many commands")
        return
    #get the search keywords
    topic = parsed_command[0]
    del parsed_command[0]
    
    
    commands = {}
    for each_command in parsed_command:
        parsed_each_command = each_command.split(" ")
        if parsed_each_command[0] != "height" or \
           parsed_each_command[0] != "width"  or \
           parsed_each_command[0] != "blur"   or \
           parsed_each_command[0] != "graycscale"  :
            
            send_message(sender_id, "unsupported command")
            return
        
        if parsed_each_command[0] == "height" or \
           parsed_each_command[0] == "width":
        
            if parsed_each_command[1] is None or \
               parsed_each_command[1] == "":
                send_message(sender_id, parsed_each_command[0] + " expects 2 arguments")
                return

            #check if [1] is %
            if parsed_each_command[1].endswith("%") is False:
                send_message(sender_id, parsed_each_command[0] + " can only take a percentile")
                return
                
            #check [1]'s number part is 1-100
            number_arg = parsed_each_command[1].split("%")[0]
            if number_arg < 1 or number_arg > 100:
                send_message(sender_id, "percentage must be between 1 to 100")
                return
                
            #now we are good to go
            commands.update({parsed_each_command[0] : parsed_each_command[1]})
            
        if parsed_each_command[0] == "blur":
            
            if parsed_each_command[1] is None or \
               parsed_each_command[1] == "":
                send_message(sender_id, parsed_each_command[0] + " expects 2 arguments")
                return

            if parsed_each_command[1].isdigit() is False:
                send_message(sender_id, "blur can only take a number")
                return
            
            #good to go
            commands.update({parsed_each_command[0] : parsed_each_command[1]})
            
        if parsed_each_command[0] == "grayscale":
            if parsed_each_command[1] or \
               parsed_each_command[1] != "":
                send_message(sender_id, "grayscale only takes 1 argument")
                return
                
            #good to go
            commands.update({parsed_each_command[0] : ""})
            
    #at here the commands should be ready
    print(commands)
    #search the actual img
    result_url = search_image_3(topic, 0)
    if result_url is None:
        send_message(sender_id, "Your image of " + topic + " cannot be found.")
    else:
        send_message(sender_id, "Here's your picture of "+ topic)
    
    #get requested img id
    requested_img_id = upload_image(result_url)
    #get editted img
    editted_url = get_imame(requested_img_id, commands)
    print(editted_url)
    send_image(sender_id, editted_url)
    return
    """
    if parsed_command[0] == ":select" :
        
        print("entered select")
        newsearch.select()        
        print("img selected " + str(newsearch.requested_img_id))
    elif parsed_command[0] == ":edit":
        #TODO handle edit commands here
        print("entered edit")
        if newsearch.topic == "":
            print("im going back")
            return newsearch
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
        if newsearch.topic == "":
            print("im going back")
            return  newsearch
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
        if newsearch.topic == "":
            print("im going back")
            return newsearch
        newsearch.next_img()

        result = search_image_3(newsearch.topic, newsearch.offset)
        if result is None:
            send_message(sender_id, "Your image of " + newsearch.topic + " cannot be found.")
        else:
            send_message(sender_id, "Showing next picture")
            newsearch.origin_url = result
            print("set origin_url to " + newsearch.origin_url)
            send_image(sender_id, result)
            print(newsearch.offset)

    elif parsed_command[0] == ":back":
        print("entered back")
        if newsearch.topic == "":
            print("im going back")
            return     newsearch
        newsearch.prev_img()
        result = search_image_3(newsearch.topic, newsearch.offset)

        send_message(sender_id, "Showing previous picture")
        newsearch.origin_url = result
        print("set origin_url to " + newsearch.origin_url)
        send_image(sender_id, result)
        print(newsearch.offset)

    else:
        # search the FUCKING IMAGE 
        print("search img")
        result = search_image_3(message_text, newsearch.offset)
        if result is None:
            send_message(sender_id, "Your image of " + message_text + " cannot be found.")
        else:
            send_message(sender_id, "Here's your picture of "+ message_text)
            newsearch = searchinfo()
            newsearch.topic = message_text
            newsearch.offset = 0
            newsearch.origin_url = result
            print("set origin_url to " + newsearch.origin_url)
            send_image(sender_id, result)
            
     
    return 
    """










