# -*- coding: utf-8 -*-
'''
    Events:
    messages,
    messaging_postbacks,
    '''
import json
from _thread import *
from flask import Flask, request
from pymessager.message import Messager, QuickReply
from utils.config import *
from utils.wit import *
from utils.api import *
from utils.ans import *

app = Flask(__name__)
client = Messager(ACCESS_TOKEN)

sender_id = ''
recipient_id = ''
text = ''

# Verify & confirms all requests can sent to bot
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
    message_entries = json.loads(request.data.decode('utf8'))['entry'][0]
    
    messaging = message_entries['messaging'][0]
    sender_id = messaging['sender']['id'] # This is user id
    
    # Message event
    if 'message' in messaging:
        message = messaging['message']
        print(message)
        
        # Start a thread here
        start_new_thread(mesgHandler, (client, sender_id, message))

    # Postback massage
    elif 'postback' in messaging:
        postback = messaging['postback']

        if '房屋詳細資料' in postback['title']:
            detail_query = createDetail()
            detail_query['id'] = postback['payload']
            displayDetail(client, sender_id, detail_query)

        elif '新增我的最愛' or '從我的最愛刪除' in postback['title']:
            
            if '新增我的最愛' in postback['title']:
                change_type = 'add'
            else:
                change_type = 'delete'
            
            house_id = postback['payload']
            changefavorate(change_type, sender_id, house_id)

            # 為了重新印出我的最愛
            start_new_thread(mesgHandler, (client, sender_id, {'text': '我的最愛'}))

    return "Message Processed"

def mesgHandler(client, sender_id, message):
    client.typing(sender_id, on=True)
    response_message = greeting_ans[randint(0,len(greeting_ans)-1)]

    rec_query = createRecommend()
    
    # Text message, parsing text from ['text']
    if 'text' in message:
        text = message['text']
        resp = wit_response(text)
        print(resp)
        
        if 'entities' in resp:
            entities = resp['entities']

            if 'sale' in entities:
                rec_query['type'] = 'sale'
                response_message = "您想買哪裡的房子呢？"

            if 'rent' in entities:
                rec_query['type'] = 'rent'
                response_message = "您想租哪裡的房子呢？"

            if 'city' in entities:
                city = entities['city'][0]['value']

                if 'area' in entities:
                    area = entities['area'][0]['value']

                    # Check area in this city existed
                    check = regionMatch(city, area)
                    if(check):
                        rec_query['city'] = city
                        rec_query['area'] = area
                        response_message = displayHouse(client, sender_id, rec_query)

                    else:
                        response_message= "此縣市沒有這個區域喔！"

                else:
                    response_message = "您想看哪區的房子呢？"

            # Search city automatically
            elif 'area' in entities and 'city' not in entities:
                rec_query['city'], rec_query['area'] = askCity(entities['area'][0]['value'])
                response_message = displayHouse(client, sender_id, rec_query)

            elif 'favorite' in entities:
                fav_query = createFavorite()
                response_message = displayFavorate(client, sender_id, fav_query)


    # Position message
    elif 'attachments' in message:
        attachments = message['attachments'][0]

        if attachments['type'] == 'location':
            rec_query['position'] = 'user'
            rec_query['lat'] = attachments['payload']['coordinates']['lat'] # Latitude
            rec_query['lng'] = attachments['payload']['coordinates']['long'] # Longttitude

            response_message = displayHouse(client, sender_id, rec_query)

        if attachments['type'] == 'image':
            response_message = '這是圖片'

            if 'sticker_id' in attachments['payload'] :
                response_message = '這是貼圖'

    client.send_text(sender_id, response_message)


if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT)

