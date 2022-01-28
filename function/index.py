
import os,re,uuid,json,boto3
from slack_sdk import WebClient
from r import *
 


client = boto3.resource('dynamodb')
TABLE = client.Table('dynamoDB-casey-reports-286a3ce')
CREATE_RAW_PATH = "/challenge"
ok = 'http 200 OK'
slack = WebClient(token=TOKEN)

def handler(event, context):
     
    if event['rawPath'] == CREATE_RAW_PATH:
        string = event['body']
        data = json.loads(string)
        e = data['event']
        user = e['user']
        if user == "U02SE97NFJ6":
            txt = e['text'].title()
            msg_id = data['event']['client_msg_id']
            split = txt.replace(".",'').split(' ')
            first = split[0]
            last = split[1]
            date = event["requestContext"]["time"]
            response = TABLE.get_item(
                Key={
                    'lastName': f"{last}",
                    'firstName': f"{first}"
                    }) 
            if txt.startswith('Get'):
                slack.chat_postMessage(channel='report-dates', text=f'{response}')
                return
            if txt.endswith('Finish'): 
                input = {
                    "lastName": f"{last}",
                    "firstName": f"{first}",
                    "dateCreated": response['Item']["dateCreated"],
                    "reportFinished": 1,
                    "dateReportFinished": date
                    }
                slack.chat_postMessage(channel='report-dates', text=f'{response}')
            else:
                input = {
                "lastName": f"{last}",
                "firstName": f"{first}",
                "dateCreated": date,
                "reportFinished": 0,
                "dateReportFinished": ''
                }
                slack.chat_postMessage(channel='report-dates', text=f'{response}')
            
            response = TABLE.put_item(Item=input)
            
        
        return ok
    
    
    
    