
from edit_img import *




class searchinfo(object):


        
    def __init__(self):
        self.sender_id = ""
        self.topic = ""
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
    
