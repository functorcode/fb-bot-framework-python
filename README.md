# fb-bot-framework-python
fb_bot_framework-python is easy to integrate facebook messanger bot framework for python. You can use it with AWS Lambda, flask ,django etc.

## Features
* Easy to integrate with AWS Lambd, flask ,django etc..
* Supports NLP
* Supports quick replies, postback, text message,actions 
(typing_on,typing_off,mark_seen)
* Supports getting started button and greeting text

## Usage

### Flask
``` python
from flask import Flask,request
import json
import requests
from fb_bot_framework import *
import bot_app


page_token="YOURPAGE_TOKEN" #change this
verification_token="YOURVERIFY_TOKEN"
app = Flask(__name__)


bot=FB_Bot_Framework(verification_token,page_token)
bot.subscribe_on_message(bot_app.on_message)
bot.subscribe_on_quick_reply(bot_app.on_quick_reply)
bot.subscribe_on_postback(bot_app.on_postback)
bot_app.set_greeting_text()
bot_app.set_getstarted_btn()
@app.route('/', methods=['GET'])
def handle_verification():
    qp=dict(request.args)
    parsed={}
    for key,val in qp.items():
        parsed.setdefault(key,val[0])
    code= bot.verify(parsed)
    if code !=None:
        return code
    else:
        return "Error",422
@app.route("/",methods=['POST'])
def handle_message():
    bot.process_message(request.json)
    return "Okay"

if __name__ == '__main__':
    app.run()
```


### AWS 

### Webhook Lambda
``` python
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
```

### Message Processing Lambda
```python
import requests
import requests
from fb_bot_framework import *
import bot_app
page_token="YOURPAGE_TOKEN" #change this
verification_token="YOUR_VERIFICATION_TOKEN" #change this
bot=FB_Bot_Framework(verification_token,page_token)
bot.subscribe_on_message(bot_app.on_message)
bot.subscribe_on_quick_reply(bot_app.on_quick_reply)
bot.subscribe_on_postback(bot_app.on_postback)
bot_app.set_greeting_text()
bot_app.set_getstarted_btn()
def lambda_handler(event, context):
  bot.process_message(event)
```

### Bot App - Handle message and reply back
``` python
import sys
sys.path.insert(0, '../')
from fb_bot_framework import *
from boto3 import client as boto3_client
lambda_client = boto3_client('lambda','us-east-1')
verification_token="YOURVERIFY_TOKEN"
page_token="YOURPAGE_TOKEN" #change this

bot=FB_Bot_Framework(verification_token,page_token)

test_button= [
    {
        "content_type": "text",
        "title": "Tell me",
        "payload": json.dumps({"cmd":"get_weather"})
    }]

def set_greeting_text():
    greetings=[{"locale":"default","text":"I can tell you today's weather forcast."}]
    bot.set_greeting_text(greetings)
def set_getstarted_btn():
    bot.set_getstarted_btn(json.dumps({"cmd":"get_started"}))

def get_first_entity(nlp,name):
    if nlp.has_key('entities'):
        if nlp['entities'].has_key(name):
            if len(nlp['entities'][name])>0:
                return nlp['entities'][name][0]
    return {}
def process_nlp(nlp):
    greetings=get_first_entity(nlp,'greetings')
    thanks=get_first_entity(nlp,'thanks')
    bye=get_first_entity(nlp,'bye')
    
    if "confidence" in greetings:
        if greetings["confidence"]>0.8:
            return "greetings"
    if "confidence" in thanks:
        if thanks["confidence"]>0.8:
            return "thanks"
    if "confidence" in bye:
        if bye["confidence"]>0.8:
            return "bye"
def on_message(userId,message):
    print "From on messaage"
    print message
    nlp_value=""
    text=message['text']


    if "nlp" in message:
        nlp_value=process_nlp(message['nlp'])
    print nlp_value
    if nlp_value=="greetings":
        bot.send_text_message(userId,"Hi there")
    elif nlp_value=="thanks":
        bot.send_text_message(userId,"No problem")
    elif nlp_value=="bye":
        bot.send_text_message(userId,"bye")
    elif text[0]=="Weather":
        bot.send_text_message(userId, "It will rain today.")
      
    else:
        bot.send_quick_replies(userId, "I can tell you today's weather forcast", test_button)

def on_postback(userId,payload_data):
    payload=json.loads(payload_data)
    if payload['cmd']=="get_started":
        bot.send_text_message(userId,"Hello")
        bot.send_quick_replies(userId,"I can tell you today's weather forcast",test_button)
def on_quick_reply(userId,payload_data):
    payload=json.loads(payload_data)
    if payload['cmd']=="get_weather":
        bot.send_text_message(userId, "It will rain today.")

```
