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





