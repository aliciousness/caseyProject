import os,re,slack,uuid,json
 


CREATE_RAW_PATH = "/challenge"
SLACK_ACCESS_TOKEN = 'xoxb-2895391715429-2911092400561-olwSyFBzi77lNdFYcMimVMAy'
APP_VERIF_TOKEN = ''
def handler(event, context):
    print(event)
    
    #bot responding to channel
    client = slack.WebClient(token=SLACK_ACCESS_TOKEN)
    client.chat_postMessage(channel='report-dates', text='This is only a test.')

    
    #takes info from body that slack post and returns the challenge key 
    if event['rawPath'] == CREATE_RAW_PATH:
        #CreatePerson Path - write to database
        print("Start Request")
        challenge = event['body']
        return challenge
    
    
    