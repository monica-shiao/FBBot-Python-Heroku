# -*- coding: utf-8 -*-
import json
from flask import Flask, request
from pymessager.message import Messager
from utils.config import *

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
        print(entry)
        for message in entry['messaging']:
            recipient_id = message['sender']['id']
            if message.get('message'):
                client.send_text(recipient_id, message['message']['text'])
    return "Message Processed"

if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT)
