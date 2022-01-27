import os,re,uuid,json,boto3,datetime 


 

client = boto3.resource('dynamodb')
TABLE = client.Table('dynamoDB-casey-reports-286a3ce')
CREATE_RAW_PATH = "/challenge"
ok = 'htttp 200 OK'

def handler(event, context):
    print(event)
    
    #takes info from body that slack post and returns the challenge key 
    if event['rawPath'] == CREATE_RAW_PATH:
        
        print("Start Request")
        string = event['body']
        data = json.loads(string)
        e = data['event']
        user = e['user']
        
        if user == "U02SE97NFJ6":
            txt = e['text']
            msg_id = data['event']['client_msg_id']
            first,last = txt.split(' ')
            date = event["requestContext"]["time"]
            if "finished" in txt:
                fin = 1
                finDate = date
                input = {
                    "lastName": f"{last}",
                    "firstName": f"{first}",
                    "reportFinished": fin,
                    "dateReportFinished": finDate
                    }
            else:
                fin = 0 
                input = {
                    "lastName": f"{last}",
                    "firstName": f"{first}",
                    "dateCreated": date,
                    "reportFinished": fin,
                    "dateReportFinished": ''
                    }
            
            response = TABLE.put_item(Item=input)
            print(response)
        
        return ok
    
    
    
    