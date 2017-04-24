from edit_img import *
from search_img import *
from send import *
from dynamodb import *
from s3 import *



def msg_handler(sender_id, message_text):
    
    
    
    ###########
    check_exist = returnList(sender_id)
    #print(check_exist)
    if check_exist == None:   
        createNewUser(sender_id)     
        print("new user created")
    ###########
    if message_text == 'list':
        print("printing all histories")
        list = returnList(sender_id)
        if  not list :
            send_message(sender_id, 'You have not searched anything yet!')
        for item in list:
            send_message(sender_id, "Here's your history search of "+item)
            send_image(sender_id, list[item])
        return
    ###########
    if message_text == 'clear':
        emptyList(sender_id)
        send_message(sender_id, "History cleared")
        return
    ###########
    parsed_command = message_text.split(":")
    print(parsed_command)
    if len(parsed_command) > 6:
        send_message(sender_id, "Too many commands")
        return
    #get the search keywords
    topic = parsed_command[0]
    del parsed_command[0]
    
    
    commands = {}
    for each_command in parsed_command:
        each_command = each_command.strip()
        print("each command is /"+each_command)
        #no leading and tailing 0
        #" ".join(each_command.split())
        
        parsed_each_command = each_command.split()
        print(parsed_each_command)
        if not parsed_each_command:
            send_message(sender_id, "wrong format")
            return
        if parsed_each_command[0] != "height" and \
           parsed_each_command[0] != "width"  and \
           parsed_each_command[0] != "blur"   and \
           parsed_each_command[0] != "grayscale"  and \
           parsed_each_command[0] != "ellipse" :
            
            send_message(sender_id, "unsupported command " + parsed_each_command[0])
            return
        
        if parsed_each_command[0] == "height" or \
           parsed_each_command[0] == "width":
            if len(parsed_each_command) < 2:
                send_message(sender_id, parsed_each_command[0] + " expects 2 arguments")
                return
            if parsed_each_command[1] is None or \
               parsed_each_command[1] == "":
                send_message(sender_id, parsed_each_command[0] + " expects 2 arguments")
                return

            #check if [1] is %
            if parsed_each_command[1].endswith("%") is False:
                send_message(sender_id, parsed_each_command[0] + " can only take a percentage")
                return
                
            #check [1]'s number part is 1-100
            number_arg = parsed_each_command[1].split("%")[0]
            if float(number_arg) < 1 or float(number_arg) > 100:
                send_message(sender_id, parsed_each_command[0] + " percentage must be between 1 to 100")
                return
                
            #now we are good to go
            commands.update({parsed_each_command[0] : parsed_each_command[1]})
            
        if parsed_each_command[0] == "blur":
          
            if len(parsed_each_command) < 2:
                send_message(sender_id, parsed_each_command[0] + " expects 2 arguments")
                return

            if  parsed_each_command[1] == "":
                send_message(sender_id, parsed_each_command[0] + " expects 2 arguments")
                return

            if parsed_each_command[1].isdigit() is False:
                send_message(sender_id, "blur can only take a number")
                return
            
            #good to go
            commands.update({parsed_each_command[0] : parsed_each_command[1]})
            
        if parsed_each_command[0] == "grayscale":
            if len(parsed_each_command) > 1:
                send_message(sender_id, "grayscale only takes 1 argument")
                return
                
            #good to go
            commands.update({parsed_each_command[0] : ""})

        if parsed_each_command[0] == "ellipse":
            if len(parsed_each_command) > 1:
                send_message(sender_id, "ellipse only takes 1 argument")
                return
            #good to go
            commands.update({parsed_each_command[0] : ""})
            commands.update({"format" : "png"})
            
    #at here the commands should be ready
    print(commands)
    #search the actual img
    
    #DONE finish the JSON parsing##########
    result_url = ''
    url_list = returnList(sender_id)
    for item in url_list:
        print(item)
        if item == topic:
            result_url = url_list[item]
            
    if result_url == '': 
        result_url, extension = search_image_3(topic, 0)
        #upload result url
        print(result_url)
        result_url, filepath = s3_handler(result_url, topic, extension)
        appendTo(sender_id, topic, result_url)
    if result_url is None:
        send_message(sender_id, "Your image of " + topic + " cannot be found.")
        return
    #######################################
    
    #only search
    if not commands :
        print("send original search img")
        send_message(sender_id, "Here's your image of "+ topic)
        send_image(sender_id, result_url)
        #send_upload_image(sender_id, filepath)
        return
        
    #get requested img id
    requested_img_id = ''
    print("uploading img")
    img_id_list = returnList(1234567890)
    for item in img_id_list['history']:
        if item == topic:
            requested_img_id = img_id_list[item]
    if not requested_img_id:
        requested_img_id = upload_image(result_url)
        appendTo(1234567890, topic, requested_img_id)
        
        
    print("request id "+requested_img_id)
    #get editted img
    editted_url = get_image(requested_img_id, commands)
    print("final url "+editted_url)
    send_message(sender_id,"Here's your edited image of " + topic)
    send_image(sender_id, editted_url)
    return











