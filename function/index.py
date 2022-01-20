import os,re,uuid,json

 


CREATE_RAW_PATH = "/challenge"


def handler(event, context):
    print(event)
    
    #takes info from body that slack post and returns the challenge key 
    if event['rawPath'] == CREATE_RAW_PATH:
        #CreatePerson Path - write to database
        print("Start Request")
        challenge = event['body']
        return challenge
    
    
    