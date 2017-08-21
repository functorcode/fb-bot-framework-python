import sys
sys.path.insert(0, '../')
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