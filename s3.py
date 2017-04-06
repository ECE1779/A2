
from __future__ import print_function
import boto3
import os
import sys

     
s3 = boto3.resource('s3', aws_access_key_id=os.environ["ACCESS_KEY_ID"], aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"])
  
  '''
  import boto3
s3 = boto3.resource('s3')
s3.meta.client.upload_file('/tmp/hello.txt', 'mybucket', 'hello.txt')
  '''
def download_file(url, keyword):

    garbage, extension = os.path.splitext(url)
    print("Downloading new image")
    r = requests.get(url)
    filepath = "/tmp/{}{}".format(keyword, extension) 
    with open(filepath, "wb") as code:
        code.write(r.content)
    return filepath, filename
    
    #s3.upload_fileobj(f1, "bucketforprj1", f1_filename)



def s3_handler(url, keyword):
    filepath, filename = download_file(url, keyword)
    
    s3.meta.client.upload_file(filepath, 'bucketforprj2', filename)
    
    image_url = "https://s3.amazonaws.com/bucketforprj1/{}".format(filename)
    return image_url
