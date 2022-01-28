import os,re,uuid,json,boto3,datetime
import __main__

 


client = boto3.resource('dynamodb')
TABLE = client.Table('dynamoDB-casey-reports-286a3ce')
CREATE_RAW_PATH = "/challenge"
ok = 'http 200 OK'

def handler(event, context):
    print(event)
    print(__main__)
    #takes info from body that slack post and returns the challenge key 
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
                # __main__.SLACK.chat_postMessage(channel='report-dates', text=f'{response}')
                return
            if txt.endswith('Finish'): 
                input = {
                    "lastName": f"{last}",
                    "firstName": f"{first}",
                    "dateCreated": response['Item']["dateCreated"],
                    "reportFinished": 1,
                    "dateReportFinished": date
                    }
                # __main__.SLACK.chat_postMessage(channel='report-dates', text=f'{response}')
            else:
                input = {
                "lastName": f"{last}",
                "firstName": f"{first}",
                "dateCreated": date,
                "reportFinished": 0,
                "dateReportFinished": ''
                }
                # __main__.SLACK.chat_postMessage(channel='report-dates', text=f'{response}')
            
            response = TABLE.put_item(Item=input)
            
        
        return ok
    
    
    
    