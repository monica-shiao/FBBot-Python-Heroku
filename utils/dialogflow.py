import apiai
import json
from config import DIALOGFLOW_TOKEN

def dialogflowResponse(text):
    ai = apiai.ApiAI(DIALOGFLOW_TOKEN)
    request = ai.text_request()
    request.lang = 'zh-TW'
    #request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    request.query = text
    response = request.getresponse()
    res = response.read().decode('utf8').replace('\n', '').replace(' ', '')
    res = json.loads(res)
    return res