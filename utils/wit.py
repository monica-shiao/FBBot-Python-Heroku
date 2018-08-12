from wit import Wit
from utils.config import WIT_ACCESS_TOKEN

client = Wit(access_token = WIT_ACCESS_TOKEN) 


# Ask House and Get Response
def wit_response(message_text):
	resp = client.message(message_text)
	return resp
