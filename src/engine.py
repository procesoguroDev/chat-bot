from send_message import send_message
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_message(message,phone_number_id):
    try:  
        sender_id = message["from"]
        send_message(sender_id, "Hey, your bot is up!", phone_number_id)
        logger.log("success")
    except Exception as e:
        logger.error(f"engine error {e}")