import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb', aws_access_key_id=os.environ["ACCESS_KEY_ID"], aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"])

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('FB_Chatbot')


def createNewUser(userID):




def appendTo(userID, keyword, url):





def removeFrom(userID, keyword):




def returnList(userID):





