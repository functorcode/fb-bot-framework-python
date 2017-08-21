import requests
import json
class FB_Bot_Framework:
    FB_MESSENGER_ENDPOINT = "https://graph.facebook.com/v2.6/me/messages"
    FB_PROFILE_ENDPOINT="https://graph.facebook.com/v2.6/me/messenger_profile"
    def __init__(self, verify_token,page_token):
        self.verify_token=verify_token
        self.page_token=page_token
        self.on_message=None
        self.on_quick_reply=None
        self.on_postback=None
        self.FB_MESSENGER_ENDPOINT=self.FB_MESSENGER_ENDPOINT+"?access_token="+page_token
        self.FB_PROFILE_ENDPOINT=self.FB_PROFILE_ENDPOINT+"?access_token="+page_token
    def post_json_req(self,url,data):
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.status_code==200:
            return True
        else:
            return False
    def set_greeting_text(self,greetings):
        data={
            "greeting":greetings
        }
        self.post_json_req(self.FB_PROFILE_ENDPOINT,data)
    def set_getstarted_btn(self,payload):
        data={
            "get_started":{
                "payload":payload
            }
        }
        self.post_json_req(self.FB_PROFILE_ENDPOINT,data)

    def send_text_message(self,userId,message):
        data={"recipient": {
                "id":userId
            },
            "message": {
                "text": message
            }
            }
        self.post_json_req(self.FB_MESSENGER_ENDPOINT,data)
    def send_quick_replies(self,userId,txt_msg,quick_replies_content):
        data={"recipient": {
                "id":userId
            },
            "message": {
                "text":txt_msg,
                "quick_replies": quick_replies_content
            }
            }
        self.post_json_req(self.FB_MESSENGER_ENDPOINT,data)
    def send_typing_on(self,userId):
        data={
             "recipient":{
                "id":userId
            },
            "sender_action":"typing_on"
            }
        self.post_json_req(self.FB_MESSENGER_ENDPOINT,data)
    def send_typing_off(self,userId):
        data={
             "recipient":{
                "id":userId
            },
            "sender_action":"typing_off"
            }
        self.post_json_req(self.FB_MESSENGER_ENDPOINT,data)
    
    def send_mark_seen(self,userId):
        data={
             "recipient":{
                "id":userId
            },
            "sender_action":"mark_seen"
            }
        self.post_json_req(self.FB_MESSENGER_ENDPOINT,data)

    def verify(self,data):
        if data['hub.verify_token']==self.verify_token:
            return data['hub.challenge']
        else:
            return None
    def subscribe_on_message(self,func):
        self.on_message=func
    def subscribe_on_quick_reply(self,func):
        self.on_quick_reply=func
    def subscribe_on_postback(self,func):
        self.on_postback=func
    def process_message(self,message):
        print message
        if message.has_key("object"):
            if message['object'] == "page":
                
                messaging=message['entry'][0]['messaging']
                for msg in messaging:
                    if msg.has_key('message'):
                        if msg['message'].has_key('quick_reply'):
                            if self.on_quick_reply!= None:
                                self.on_quick_reply(msg['sender']['id'],msg['message']['quick_reply']['payload'])

                        elif  msg['message'].has_key('text') :
                            if self.on_message!=None :
                                self.on_message(msg['sender']['id'],msg['message'])
                    elif msg.has_key("postback"):
                        if self.on_postback!= None:
                            self.on_postback(msg['sender']['id'],msg['postback']['payload'])
        else:
            return None
    
