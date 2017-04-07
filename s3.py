
from __future__ import print_function
import boto3
import os
import sys
import requests
import urllib
     
s3 = boto3.resource('s3', aws_access_key_id=os.environ["ACCESS_KEY_ID"], aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"])
  

def download_file(url, keyword, extension):

    #garbage, extension = os.path.splitext(url)
    print("Downloading new image")
    r = requests.get(url)
    if extension == "jpeg":
        extension = "jpg"
    filepath = "/tmp/{}.{}".format(keyword, extension) 
    filename = "{}.{}".format(keyword, extension)
    with open(filepath, "wb") as code:
        code.write(r.content)
    print("Download finished")
    return filepath, filename
    
    #s3.upload_fileobj(f1, "bucketforprj1", f1_filename)



def s3_handler(url, keyword, extension):
    filepath, filename = download_file(url, keyword, extension)
    
    s3.meta.client.upload_file(filepath, 'bucketforprj2', filename, ExtraArgs={'ContentType': 'image/{}'.format(extension)} )
    filename = urllib.quote(filename)
    print(filename)
    image_url = "http://s3.amazonaws.com/bucketforprj2/{}".format(filename)
    return image_url, filepath
