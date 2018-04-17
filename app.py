# -*- coding: utf-8 -*-
import json
from flask import Flask, request
from pymessager.message import Messager
from utils.config import *
import apiai

ai = apiai.ApiAI(DIALOGFLOW_TOKEN)


app = Flask(__name__)

client = Messager(ACCESS_TOKEN)

# Verify & confirms all requests can sent to bot.
@app.route('/', methods=['GET'])
def fb_webhook():
    verify_token = request.args.get('hub.verify_token')
    if verify_token == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else:
        return '200'

'''
# Receive the message
@app.route('/', methods=['POST'])
def fb_receive_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        print(entry)
        for message in entry['messaging']:
            recipient_id = message['sender']['id']
            if message.get('message'):
                send_response(recipient_id, parse_user_message(message_text))
                # client.send_text(recipient_id, parse_user_message(message_text))
    return "Message Processed"

'''

@app.route('/', methods=['POST'])
def handle_message():
    '''
        Handle messages sent by facebook messenger to the applicaiton
        '''
    data = request.get_json()
    print("data" + data)
    if data["object"] == "page":
        print("input the page")
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]
                    print("The message_text is " + message_text)
                    send_response(sender_id, parse_user_text(message_text))
    return "ok"


def parse_user_text(user_text):
    '''
        Send the message to API AI which invokes an intent
        and sends the response accordingly
        '''
    request = ai.text_request()
    request.query = user_text
    response = json.loads(request.getresponse().read().decode('utf-8'))
    responseStatus = response['status']['code']
    print("responseStatus is : " + responseStatus)
    if (responseStatus == 200):
        print("API AI response", response['result']['fulfillment']['speech'])
    else:
        return ("Sorry, I couldn't understand that question")


def send_response(sender_id, message_text):
    url = "https://graph.facebook.com/v2.6/me/messages"
    params = {'access_token': ACCESS_TOKEN}
    headers = {'Content-Type': 'application/json'}
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': message_text}
    }
    response = requests.post(url, params=params, headers=headers,json=data)
    return response


'''

def parse_natural_event(self, event, session_id, contexts):
    e = apiai.events.Event(event)
    request = ai.event_request(e)
    request.session_id = session_id  # unique for each user
    request.contexts = contexts    # a list
    response = json.loads(request.getresponse().read().decode(‘utf-8’))
    return response





# Receive the message
@app.route('/', methods=['POST'])
def fb_receive_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        print(entry)
        for message in entry['messaging']:
            recipient_id = message['sender']['id']
            if message.get('message'):
                client.send_text(recipient_id, message['message']['text'])
    return "Message Processed"
'''

if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT)
