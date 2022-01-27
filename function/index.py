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
            txt = e['text'].title()
            msg_id = data['event']['client_msg_id']
            split = txt.replace(".",'').split(' ')
            first = split[0]
            last = split[1]
            date = event["requestContext"]["time"]
            if "Finished" in txt: 
                response = TABLE.get_item(
                    Key={
                        'lastName': f"{last}",
                        'firstName': f"{first}"
                    }
                ) 
                input = {
                    "lastName": f"{last}",
                    "firstName": f"{first}",
                    "dateCreated": response['Item']["dateCreated"],
                    "reportFinished": 1,
                    "dateReportFinished": date
                    }
            else:
                input = {
                "lastName": f"{last}",
                "firstName": f"{first}",
                "dateCreated": date,
                "reportFinished": 0,
                "dateReportFinished": ''
                }
            
            response = TABLE.put_item(Item=input)
            
        
        return ok
    
    
    
    