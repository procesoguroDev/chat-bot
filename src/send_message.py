import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
BASE_URL = os.getenv("BASE_URL_WEBHOOK")

def  send_message(to, phone_number_id):
    try:
        # message_send = """No quiero ser egoísta y por ello te pido que no me guardes luto, que no te apenes por mí, que rehagas tu vida lo más pronto posible y que no me eches en falta pues yo siempre estaré contigo en cada momento de tu vida. Que seas muy feliz y que hagas realidad todos tus sueños, ya que los míos se cumplieron cuando me dejaste amarte. Quiero que sepas que mis últimos pensamientos son para ti y que siempre te querré y cuidaré allá donde esté."""
       
        url = f"{BASE_URL}/{phone_number_id}/messages"

        headers =  {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": "524432552079",
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {
                    "code": "en_US"
                }
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            logger.error(f"Failed to send message to {to}. Response: {response.status_code} {response.text}")
            return
        logger.log(f"Message sent to {to}.")
    except Exception as e:
        print("send message",e)
        logger.error(f"server error: {e}")
