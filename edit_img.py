import http.client, urllib.request, urllib.parse, urllib.error, base64, json

########### ImageResizer ###########
def upload_image(url):
    # https://api.imageresizer.io/images?key=8306ec405392ace375c33449ab79acbdcea54890&url=https://upload.wikimedia.org/wikipedia/commons/6/65/Tesla_Model_S_Indoors.jpg
    # this should return an image url
    params = urllib.parse.urlencode({
        'key': '8306ec405392ace375c33449ab79acbdcea54890',
        'url': url,
    })

    try:
        conn = http.client.HTTPSConnection('api.imageresizer.io')
        conn.request("GET", "/images?%s" % params)
        response = conn.getresponse()

        data = response.read()
        json_data = json.loads(data)
        while json_data["success"] == False:
            response = conn.getresponse()
            data = response.read()
            json_data = json.loads(data)
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    
    print(json_data)

    if json_data["success"] == False:
        return None
    else:
        return json_data["response"]["id"]

def get_image(img_id, command):
    head = "https://im.ages.io/"
    print(img_id)
    #img_id
    #"?"
    params = urllib.parse.urlencode(command)

    img_url = head + img_id + "?" + params
    return img_url

support_commands = {"height 100%\nwidth 100%\ncrop heightxwidth\nellipse\nblur 10\ngrayscale"}

####################################
