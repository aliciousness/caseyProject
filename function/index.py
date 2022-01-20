import os,re,uuid,json

 


CREATE_RAW_PATH = "/challenge"

ok = 'htttp 200 OK'
def handler(event, context):
    #print(event)
    
    #takes info from body that slack post and returns the challenge key 
    if event['rawPath'] == CREATE_RAW_PATH:
        
        print("Start Request")
        body = event['body']
        # print('event', event, type(event['body']))
        print('EVENT TYPE', type(event['body']),event)
        return ok
    
    
    
    