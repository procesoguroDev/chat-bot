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
