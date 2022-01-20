import os,re,uuid,json

 


CREATE_RAW_PATH = "/challenge"

ok = 'htttp 200 OK'
def handler(event, context):
    print(event)
    
    #takes info from body that slack post and returns the challenge key 
    if event['rawPath'] == CREATE_RAW_PATH:
        
        print("Start Request")
        string = event['body']
        data = json.loads(string)
        user = data['event']['user']
        txt = data['event']['text']
        msg_id = data['event']['client_msg_id']
        
        return ok
    
    
    
    