# Property Voice Assistant

A full-stack AI-powered telephony assistant built with **Django + React**.  
Voice callers can ask questions about property listings and receive spoken answers via Twilio.

---

## 🗂 Project Layout

```
telephony agent/
├── backend/          # Django + DRF API + Twilio webhooks
└── frontend/         # React (Vite) property listing UI
```

---

## ⚡ Quick Start

### 1 — Backend

```bash
cd backend

# Create & activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Copy env template and fill in your credentials
copy .env.example .env

# Apply migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Seed sample property data
python manage.py seed_properties

# Start dev server
python manage.py runserver
```

Backend available at: `http://127.0.0.1:8000`

### 2 — Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: `http://localhost:5173`

---

## 🔑 Environment Variables

Copy `backend/.env.example` → `backend/.env` and fill in:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | PostgreSQL connection string |
| `TWILIO_ACCOUNT_SID` | From Twilio console |
| `TWILIO_AUTH_TOKEN` | From Twilio console |
| `TWILIO_PHONE_NUMBER` | Your Twilio number |

---

## 📡 API Endpoints

| Method | URL | Description |
|---|---|---|
| `GET` | `/api/properties/` | List all properties (supports `?search=`) |
| `GET` | `/api/properties/<id>/` | Single property detail |
| `POST` | `/voice/` | Twilio inbound call webhook |
| `POST` | `/process-speech/` | Speech-to-intent-to-TTS callback |

---

## 📞 Twilio Setup

1. In the [Twilio Console](https://console.twilio.com), set your phone number's **Voice Webhook** to:
   ```
   https://<your-public-url>/voice/
   ```
2. Use [ngrok](https://ngrok.com) locally: `ngrok http 8000`
3. Update your Twilio webhook URL with the ngrok HTTPS URL.

---

## 🧠 AI Agent Flow

```
Caller speaks → Twilio STT → POST /process-speech/
  → detect_intent() → DB lookup → natural language response
  → Twilio TTS → spoken back to caller
```

Supported intents: **price**, **location**, **area**, **amenities**, **bedrooms**, **description**.

---

## 🛠 Admin

Visit `http://127.0.0.1:8000/admin/` to manage properties and view conversation logs.
