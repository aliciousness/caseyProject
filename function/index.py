import json
import uuid


CREATE_RAW_PATH = "/challenge"

def handler(event, context):
    print(event)
    
    if event['rawPath'] == CREATE_RAW_PATH:
        #CreatePerson Path - write to database
        print("Start Request for CreatePerson")
        challenge = event['body']
        print(challenge)
        return challenge