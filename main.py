from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, PlainTextResponse
import httpx
import uvicorn
app = FastAPI()
from config import NGROK_TOKEN, ENABLE_NGROK

# URL base para enviar mensajes
# WHATSAPP_API_URL = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
""" 
@app.get("/webhook")
async def verify_webhook(request: Request):
    # Validación del webhook
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        # Return the challenge exactly as received (Facebook expects the same value)
        if challenge is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing challenge")
        return PlainTextResponse(content=str(challenge))
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Verification token mismatch",
    )

@app.post("/webhook")
async def webhook(request: Request):
    # Recibe mensajes entrantes
    data = await request.json()
    try:
        # Extrae el mensaje y el número del remitente
        entry = None
        try:
            entry = data.get("entry", [])[0].get("changes", [])[0].get("value", {})
        except Exception:
            entry = {}

        if not entry:
            logger.debug("Webhook entry vacío o estructura inesperada: %s", data)
            return JSONResponse(content={"status": "ignored"})

        # Manejar solo mensajes de texto por ahora
        messages = entry.get("messages")
        if messages and isinstance(messages, list) and len(messages) > 0:
            msg = messages[0]
            msg_type = msg.get("type")
            sender = msg.get("from")

            if msg_type == "text":
                message = msg.get("text", {}).get("body", "")
                # Lógica del chatbot: Respuesta de eco
                response_message = f"Recibí: {message}"

                # Envía respuesta usando la API de WhatsApp de forma asíncrona
                headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "messaging_product": "whatsapp",
                    "to": sender,
                    "type": "text",
                    "text": {"body": response_message},
                }

                async with httpx.AsyncClient(timeout=10.0) as client:
                    try:
                        resp = await client.post(WHATSAPP_API_URL, json=payload, headers=headers)
                        if resp.status_code >= 200 and resp.status_code < 300:
                            logger.info("Mensaje enviado a %s", sender)
                        else:
                            logger.error("Error al enviar mensaje: %s", resp.text)
                    except Exception as exc:
                        logger.exception("Excepción al enviar mensaje: %s", exc)
            else:
                logger.info("Mensaje de tipo no soportado recibido: %s", msg_type)
        else:
            logger.debug("No hay mensajes para procesar en entry: %s", entry)

        return JSONResponse(content={"status": "ok"})
    except Exception as e:
        print(f"Error procesando webhook: {e}")
        raise HTTPException(status_code=400, detail="Error procesando mensaje")
 """
@app.get("/")
async def root():
    return {"mensaje": "Chatbot WhatsApp activo!"}

if __name__ == "__main__":
    # Inicia Ngrok para exponer el servidor local si está habilitado
    try:
        if ENABLE_NGROK and str(ENABLE_NGROK).lower() in ("1", "true", "yes", "y"):
            if NGROK_TOKEN:
                try:
                    from pyngrok import ngrok
                except Exception:
                    print("pyngrok no está instalado. Instale 'pyngrok' o desactive ENABLE_NGROK en .env")
                else:
                    public_url = ngrok.connect(8000, authtoken=NGROK_TOKEN)
                    print(f"URL pública para webhook: {public_url}/webhook")
            else:
                print("NGROK_TOKEN no encontrado en variables de entorno. No se iniciará ngrok.")
        else:
            print("Ngrok deshabilitado por ENABLE_NGROK")
    except Exception as e:
        print("grok error:", e)
        print("Error comprobando configuración de ngrok. Continuando sin ngrok.")

    # Inicia el servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)