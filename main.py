from fastapi import FastAPI
from app.routes import webhook

app = FastAPI(
    title="Footy Blitz WhatsApp Bot",
    description="AI-powered WhatsApp order-taking bot for Footy Blitz shoe shop",
    version="1.0.0"
)

app.include_router(webhook.router)

@app.get("/")
def root():
    return {"status": "Footy Blitz Bot is running 🥿"}