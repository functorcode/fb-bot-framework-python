VERIFY_TOKEN = "YOUR_VERIFICATION_TOKEN" #change this
from boto3 import client as boto3_client
import json
lambda_client = boto3_client('lambda')
def lambda_handler(event, context):
    print json.dumps(event)
    if event['queryStringParameters']!=None:
        print "here"
        verify_token=event['queryStringParameters']['hub.verify_token']
        if(verify_token== VERIFY_TOKEN):
            challenge=event['queryStringParameters']['hub.challenge']
            return {"statusCode":200,"body":challenge}
        else:
            return {"body":"Error, wrong validation token","statusCode":422}
    else:
        msg =event['body']
        invoke_response = lambda_client.invoke(FunctionName="FUNCTION_NAME",
                                           InvocationType='Event',
                                           Payload=json.dumps(msg))
        print "Invoked"
        return {"statusCode":200}
    
    