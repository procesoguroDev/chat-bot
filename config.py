import os
from dotenv import load_dotenv

load_dotenv()


def _get_env(key, default=None):
	"""Lee una variable de entorno y sanea espacios y comillas laterales."""
	val = os.getenv(key, default)
	if isinstance(val, str):
		# Elimina espacios en los extremos y comillas simples/dobles sobrantes
		val = val.strip().strip('"').strip("'")
	return val


VERIFY_TOKEN = _get_env("WHATSAPP_VERIFY_TOKEN")
ACCESS_TOKEN = _get_env("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = _get_env("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_BASE_API_URL = _get_env("WHATSAPP_API_URL")
NGROK_TOKEN = _get_env("NGROK_TOKEN")
# Permite desactivar ngrok si se quiere (por ejemplo en producción)
ENABLE_NGROK = _get_env("ENABLE_NGROK") or "true"

# Construye la URL completa de la API de WhatsApp si hay base y phone id
WHATSAPP_API_URL = None
if WHATSAPP_BASE_API_URL and PHONE_NUMBER_ID:
	WHATSAPP_API_URL = f"{WHATSAPP_BASE_API_URL.rstrip('/')}/{PHONE_NUMBER_ID}/messages"
