# Footy Blitz WhatsApp Bot

An AI-powered WhatsApp order-taking bot for Footy Blitz shoe shop, built with FastAPI and Twilio. Supports both Claude (Anthropic) and OpenAI — switchable with a single line in your `.env`.

---

## How It Works

When a customer sends a WhatsApp message, Twilio forwards it to your server. FastAPI receives it, passes the conversation history to your chosen AI (Claude or OpenAI), and sends the reply back to the customer via Twilio — all in a few seconds.

```
Customer (WhatsApp) → Twilio → POST /webhook → AI (Claude/OpenAI) → Reply → Customer
```

---

## Project Structure

```
footy_blitz_bot/
├── main.py                  # Starts the FastAPI app, registers routes
├── requirements.txt         # Python dependencies
├── .env.example             # Copy to .env and fill in your keys
└── app/
    ├── config.py            # Loads all settings from .env
    ├── prompt.py            # Bot personality, product catalog, order rules
    ├── session.py           # In-memory conversation history per customer
    ├── ai_provider.py       # Switchable Claude / OpenAI handler
    └── routes/
        └── webhook.py       # POST /webhook endpoint (Twilio) + GET /health
```

### File Responsibilities

| File | What it does |
|---|---|
| `main.py` | Creates the FastAPI app and plugs in the webhook router |
| `config.py` | Reads `.env` once and provides typed settings to all other files |
| `prompt.py` | Contains the full system prompt — the bot's rules and product catalog |
| `session.py` | Stores each customer's conversation history, keyed by phone number |
| `ai_provider.py` | Routes to Claude or OpenAI based on `AI_PROVIDER` in `.env` |
| `webhook.py` | Receives Twilio POST requests, calls the AI, returns TwiML replies |

---

## Prerequisites

- Python 3.10+
- A [Twilio account](https://www.twilio.com) with WhatsApp Sandbox enabled
- An [Anthropic API key](https://console.anthropic.com) and/or [OpenAI API key](https://platform.openai.com)
- [ngrok](https://ngrok.com) (for local testing)

---

## Setup

### 1. Clone the repo and create a virtual environment

```bash
git clone https://github.com/your-username/footy-blitz-bot.git
cd footy-blitz-bot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your environment

```bash
cp .env.example .env
```

Open `.env` and fill in your credentials:

```env
AI_PROVIDER=claude               # Switch to "openai" anytime

ANTHROPIC_API_KEY=sk-ant-...     # From console.anthropic.com
OPENAI_API_KEY=sk-...            # From platform.openai.com
OPENAI_MODEL=gpt-4o

TWILIO_ACCOUNT_SID=ACxxxxxxxx    # From console.twilio.com
TWILIO_AUTH_TOKEN=xxxxxxxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 4. Run the server

```bash
uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000` — you should see:
```json
{"status": "Footy Blitz Bot is running 🥿"}
```

### 5. Expose your server with ngrok

In a new terminal:

```bash
ngrok http 8000
```

Copy the HTTPS URL it gives you, e.g. `https://abc123.ngrok.io`

### 6. Connect Twilio

1. Go to [console.twilio.com](https://console.twilio.com)
2. Navigate to **Messaging → Try it out → Send a WhatsApp message**
3. Open your **Sandbox Settings**
4. Set the webhook URL to: `https://abc123.ngrok.io/webhook`
5. Set the method to **POST**
6. Save

---

## Testing

Send a WhatsApp message to your Twilio sandbox number. The bot should greet you as a Footy Blitz customer.

Try a full order flow:
1. Ask about products
2. Pick an item
3. Provide your name, phone, and delivery address
4. Confirm the order summary with **YES**

---

## Switching AI Provider

Change one line in `.env` — no code changes needed:

```env
AI_PROVIDER=claude    # Use Anthropic Claude (default)
AI_PROVIDER=openai    # Use OpenAI GPT-4o
```

Restart the server after changing.

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/webhook` | Receives incoming WhatsApp messages from Twilio |
| `GET` | `/health` | Returns `{"status": "ok"}` — confirms server is up |
| `GET` | `/` | Root status check |

---

## Customisation

### Adding products

Open `app/prompt.py` and update the product catalog section:

```
## Product Catalog
1. Plain Oxford John Foster Shoes - GHS 300
2. Nike Airforce 1 - GHS 350 (Available in all colors)
3. Adidas Sambas - GHS 500 (Available in all colors)
4. Your New Product - GHS XXX - Description here
```

### Changing the bot's tone or rules

All bot behaviour is controlled by the `SYSTEM_PROMPT` in `app/prompt.py`. Edit the rules, greeting style, order format, or business info there.

---

## Production Notes

- **Session storage is in-memory** — conversation history is lost if the server restarts. For production, replace `app/session.py` with a Redis-backed store.
- **Use a proper host** — deploy to Railway, Render, or a VPS instead of running ngrok locally.
- **Secure your webhook** — add Twilio request signature validation to prevent fake POST requests.
- **Environment variables** — never commit your `.env` file. Add it to `.gitignore`.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com) — web framework
- [Twilio](https://www.twilio.com/docs/whatsapp) — WhatsApp messaging
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) — Claude API
- [OpenAI SDK](https://github.com/openai/openai-python) — GPT-4o API
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — environment config
- [uvicorn](https://www.uvicorn.org) — ASGI server

---

## License

MIT