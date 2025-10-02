# GenAI Customer Service Platform

An advanced GenAI-powered platform for multilingual customer inquiries (Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati). Handles text chat with context, intent detection, sentiment analysis, auto-resolution (KB), escalation (human handoff), follow-ups, and analytics. Backend: Flask + Google Gemini + PostgreSQL. Frontend: React (dark cyan theme, multi-page).


# Features
- **Multilingual Chat**: Gemini detects/responds in Indian languages.
- **Context & Personalization**: History in prompts, user profile (name, industry).
- **Intent/Sentiment**: Classifies queries/complaints/escalations, scores 0-1.
- **Auto-Resolution**: KB for FAQs (banking/telecom/e-commerce/utilities).
- **Escalation**: Low sentiment → Handoff with summary.
- **Follow-Ups**: Post-chat surveys (mock SMS/email).
- **Analytics**: Avg sentiment, escalation rate, total convos.
- **UI**: Dark theme, animations, responsive multi-page (Home/Chat/Analytics).

# Quick Start
# Backend
1. Clone repo.
2. `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`, set `GOOGLE_API_KEY=your_key` and `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/genai_db`.
4. `python backend/init_db.py` (setup DB).
5. `python -m backend.app` (runs on localhost:5000).

### Frontend
1. `cd frontend`.
2. `npm install`.
3. `npm start` (runs on localhost:3000, proxies to backend).

## Test Flow
1. Home → "Start Chatting" → /chat.
2. English: "Account balance?" → KB resolve + badges.
3. Hindi: Sample lock query → Escalation alert.
4. Analytics: Fetch metrics.

## Tech Stack
- **Backend**: Flask, SQLAlchemy (PostgreSQL), Google Gemini (PaLM successor).
- **Frontend**: React, React Router, Framer Motion, tsParticles.
- **External APIs**: Gemini (conversation), mock SMTP/SMS (follow-ups; max 3).

## License
MIT. © 2025 Your Name.