
import re,uuid,json,boto3,os
from subprocess import call
from slack_sdk import WebClient

 


client = boto3.resource('dynamodb')
TABLE = client.Table('dynamoDB-casey-reports-286a3ce')
CREATE_RAW_PATH = "/challenge"
ok = 'http 200 OK'
slack = WebClient(token=os.environ.get("TOKEN"))

def formatter(c):
    d = json.loads(c['Item']) #error here try adding the whole payload to json
    finishedate = d["dateReportFinsihed"]
    createdate = d['dateCreated']
    finished = d['reportFinished']
    lastname = d['lastName']
    firstname = d['firstName']
    
    if finished == 0: 
        return f"{firstname} {lastname} report is not finished. the report was created on {createdate}"
    if finished == 1:
        return f"{firstname} {lastname} report is finished. the report was created on {createdate} and was submitted on {finishedate}"


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
            call = TABLE.get_item(
                Key={
                    'lastName': f"{last}",
                    'firstName': f"{first}"
                    }) 
            
            
            if txt.startswith('Get'):
                slack.chat_postMessage(channel='report-dates', text=f'{formatter(call)}')
                return
            
            if txt.endswith('Finish'): 
                input = {
                    "lastName": f"{last}",
                    "firstName": f"{first}",
                    "dateCreated": call['Item']["dateCreated"],
                    "reportFinished": 1,
                    "dateReportFinished": date
                    }
                slack.chat_postMessage(channel='report-dates', text=f'{formatter(call)}')
            
            else:
                input = {
                "lastName": f"{last}",
                "firstName": f"{first}",
                "dateCreated": date,
                "reportFinished": 0,
                "dateReportFinished": ''
                }
                slack.chat_postMessage(channel='report-dates', text=f'{formatter(call)}')
            
            response = TABLE.put_item(Item=input)
            
        
        return ok
    
    
    
    