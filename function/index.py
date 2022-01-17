import json
import uuid

GET_RAW_PATH = "/getPerson"
CREATE_RAW_PATH = "/createPerson"

def lambda_handler(event, context):
    print(event)
    
    if event['rawPath'] == CREATE_RAW_PATH:
        #CreatePerson Path - write to database
        print("Start Request for CreatePerson")
        challenge = event['body']
        return challenge