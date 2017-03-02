
########### Bing Search ############
########### Python 2.7 #############
#import http.client, urllib.request, urllib.parse, urllib.error, base64
import httplib, urllib, base64, json

def search_image_2(q, offset):


 
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
        'safeSearch': 'Moderate',
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

    if json_data["value"]["0"] is None:
        return None
    else:
        return json_data["value"][0]["contentUrl"]

####################################
########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, json


def search_image_3(q, offset):
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'b23854bc1dc24ebcb32a94577b19b1c6',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'q': 'cats',
        'count': '1',
        'offset': offset,
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
    })

    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    json_data = json.loads(data)
    #print(json_data)

    if json_data["value"]["0"] is None:
        return None
    else:
        return json_data["value"][0]["contentUrl"]

####################################

