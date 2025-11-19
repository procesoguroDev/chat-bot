from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

app = FastAPI()


# =========================================
# 1) VERIFICACIÓN DEL WEBHOOK (GET)
# =========================================
@app.get("/webhook")
async def verify(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Token inválido", status_code=403)


# =========================================
# 2) WEBHOOK PARA MENSAJES (POST)
# =========================================
@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()

    try:
        entry = body["entry"][0]["changes"][0]["value"]

        # Checar si es mensaje
        if "messages" in entry:
            message = entry["messages"][0]
            sender = message["from"]                 # Número del usuario
            text = message["text"]["body"]           # Texto del mensaje

            print(f"Mensaje recibido de {sender}: {text}")

            # Obtener respuesta del bot
            reply_text = bot_logic(text)

            # Enviar respuesta
            send_message(sender, reply_text)

    except Exception as e:
        print("Error procesando mensaje:", e)

    return JSONResponse({"status": "ok"})


# =========================================
# 3) LÓGICA DEL CHATBOT
# =========================================
def bot_logic(msg: str) -> str:
    msg = msg.lower()

    if "hola" in msg:
        return "¡Hola! 👋 Soy tu bot de WhatsApp con FastAPI.\nEscribe *menu* para ver opciones."
    elif "menu" in msg:
        return "📌 *Menú*\n1️⃣ Información\n2️⃣ Soporte\n3️⃣ Horarios"
    elif msg == "1":
        return "ℹ️ Información: Este es un bot hecho con FastAPI y WhatsApp Cloud API."
    elif msg == "2":
        return "🛠 Soporte: ¿En qué puedo ayudarte?"
    elif msg == "3":
        return "⏰ Horarios: Lunes a viernes de 9am a 6pm."
    else:
        return "No entendí 😅. Escribe *menu* para ver opciones."


# =========================================
# 4) ENVIAR MENSAJE CON LA API DE META
# =========================================
def send_message(to: str, message: str):
    url = f"https://graph.facebook.com/v20.0/{WHATSAPP_PHONE_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message},
    }

    response = requests.post(url, headers=headers, json=data)
    print("Respuesta Meta:", response.status_code, response.text)
