import json
import uuid


CREATE_RAW_PATH = "/challenge"

def lambda_handler(event, context):
    print(event)
    
    if event['rawPath'] == CREATE_RAW_PATH:
        #CreatePerson Path - write to database
        print("Start Request for CreatePerson")
        challenge = event['body']
        return challenge