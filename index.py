
import re,uuid,json,boto3,os,blah
from slack_sdk import WebClient

#to update the zip package---
#zip -g packages.zip index.py
 
client = boto3.resource('dynamodb')
TABLE = client.Table('dynamoDB-casey-reports-286a3ce')
CREATE_RAW_PATH = "/challenge"
ok = 'http 200 OK'
slack = WebClient(token=os.environ.get("TOKEN"))

def slack_message(string):
    return slack.chat_postMessage(channel='report-dates', text=string)



def handler(event, context):
    
    data = json.loads(event["body"])
    #return data['challenge']
    
    if event['rawPath'] == CREATE_RAW_PATH:
        
        e = data['event']
        user = e['user']    
        txt = e['text'].title()
        
        
        if txt == "Help":
            slack_message(blah.help_message)
            return
                    
        if user == blah.casey: 
            msg_id = data['event']['client_msg_id']
            split = txt.replace(".",'').split(' ')
            first = split[1]
            last = split[2]
            date = event["requestContext"]["time"]
            call = TABLE.get_item(
                Key={
                    "lastName": last,
                    "firstName": first
                    }) 
            

            
            
            if txt.startswith("Get"):
                item = call['Item']
                d = item['dateCreated']
                f =item['dateReportFinished']
                
                slack_message(f'{first} {last} report start date is {d[:11]}, 60 days from this date is {blah.sixty(d)} their report finish date:') 
                slack_message(f if not f == '' else "sorry the report was not submitted to be finished yet")
                return
                
            
            elif txt.startswith('Finish'): 
                input = {
                    "lastName": f"{last}",
                    "firstName": f"{first}",
                    "dateCreated": call['Item']["dateCreated"],
                    "dateReportFinished": date
                    }
                TABLE.put_item(Item=input)
                slack_message(f'CONGRATS YOU FINISHED {first} {last}!')
                return
            
            elif txt.startswith("New"):
                input = {
                    "lastName": f"{last}",
                    "firstName": f"{first}",
                    "dateCreated": date,
                    "dateReportFinished": ''
                }
                TABLE.put_item(Item=input)
                slack_message('RECEIVED!')
                return 
       
    return data['challenge']
    
    
    
    