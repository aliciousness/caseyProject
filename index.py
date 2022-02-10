
import re,uuid,json,boto3,os
from subprocess import call
from slack_sdk import WebClient

 


client = boto3.resource('dynamodb')
TABLE = client.Table('dynamoDB-casey-reports-286a3ce')
CREATE_RAW_PATH = "/challenge"
ok = 'http 200 OK'
slack = WebClient(token=os.environ.get("TOKEN"))




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
                    "lastName": last,
                    "firstName": first
                    }) 
            
            d = str(call)
            # g = json.loads(d)
            # print(g)
            
            if txt.endswith('Get'):
                slack.chat_postMessage(channel='report-dates', text=f'{d}')
                return
                
            
            elif txt.endswith('Finish'): 
                input = {
                    "lastName": f"{last}",
                    "firstName": f"{first}",
                    "dateCreated": call['Item']["dateCreated"],
                    "dateReportFinished": date
                    }
                slack.chat_postMessage(channel='report-dates', text='DONE')
                return
            
            else:
                input = {
                "lastName": f"{last}",
                "firstName": f"{first}",
                "dateCreated": date,
                "dateReportFinished": ''
                }
                # slack.chat_postMessage(channel='report-dates', text=f'{formatter(call)}')
            
            TABLE.put_item(Item=input)
            
       
        return ok
    
    
    
    