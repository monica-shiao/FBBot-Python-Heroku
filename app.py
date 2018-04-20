# -*- coding: utf-8 -*-
import json
from flask import Flask, request
from pymessager.message import Messager, QuickReply
from utils.config import *
from utils.dialogflow import *

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

# Receive the message
@app.route('/', methods=['POST'])
def fb_receive_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        #print(entry)
        for message in entry['messaging']:
            recipient_id = message['sender']['id']
            if message.get('message'):
                client.send_quick_replies(recipient_id, "House",
                                          [QuickReply("Get Recommend", "Hello world"),
                                           QuickReply("House Detail","House Detail")])
                #res = getRecommend()
                # client.send_text(recipient_id, res['city'])
                #res = dialogflowResponse(message['message']['text'])
                #client.send_text(recipient_id, res['result']['fulfillment']['speech'])
    return "Message Processed"


#@app.route('/recommend', methods=['POST'])
def getRecommend():
    query = {
        'userid': '1835096909836936',
        'searchType': 'sale',
        'orderBy': 'score',
        'position': 'selected',
        'order': '1',
        'lat': '0',
        'lng': '0',
        'city': '臺北市',
        'area': '中正區',
        'minBuy': '0',
        'maxBuy': '999',
        'minRent': '1',
        'maxRent': '99999',
        'house': '1',
        'function': '1',
        'environment': '1'
    }
    '''
    if query['order'] not in ['0', '1']:
        return "wrong by order"
    
    if query['searchType'] not in ['sale', 'rent']:
        return "wrong by searchType"
    
    if query['orderBy'] not in ['price', 'score']:
        return "wrong by orderBy"
    
    if query['position'] not in ['user', 'selected']:
        return "wrong by position"
    '''
    #print(json.dumps(query, indent = 4))
    return query


if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT)
