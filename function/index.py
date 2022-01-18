import json
import uuid


CREATE_RAW_PATH = "/challenge"

EVENT_SUB = "/eventSub"

def handler(event, context):
    print(event)
    
    #takes info from body that slack post and returns the challenge key 
    if event['rawPath'] == CREATE_RAW_PATH:
        #CreatePerson Path - write to database
        print("Start Request")
        challenge = event['body']
        return challenge
    
    if event['rawPath'] == EVENT_SUB:
        print('It worked!')