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
