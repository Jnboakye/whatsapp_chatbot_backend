from fastapi import APIRouter, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

from app import session
from app.ai_provider import get_ai_response

router = APIRouter()


@router.post("/webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),      # Sender's WhatsApp number e.g. whatsapp:+233xxxxxxx
    Body: str = Form(...),      # Message text from user
):
    phone = From.strip()
    user_message = Body.strip()

    # 1. Append incoming user message to session history
    session.add_message(phone, "user", user_message)

    # 2. Get full history and send to AI
    history = session.get_history(phone)
    ai_reply = await get_ai_response(history)

    # 3. Save assistant reply to session
    session.add_message(phone, "assistant", ai_reply)

    # 4. Return TwiML response to Twilio
    twiml = MessagingResponse()
    twiml.message(ai_reply)
    return str(twiml)


@router.get("/health")
def health_check():
    return {"status": "ok", "bot": "Footy Blitz"}