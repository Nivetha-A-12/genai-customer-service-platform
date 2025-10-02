# backend/knowledge_base.py
"""
Simple JSON-like Knowledge Base for auto-resolution.
Key: intent + keyword, Value: resolution text (multilingual via Gemini).
Supports industries: banking, telecom, etc.
"""

KB = {
    "banking": {
        "query_balance": {
            "keywords": ["balance", "account balance", "खाता बैलेंस"],
            "resolution": "To check your balance, log in to the app with your credentials or call 1800-BANK-HELP. If issues, provide account #."
        },
        "complaint_lock": {
            "keywords": ["locked", "account lock", "लॉक", "खाता लॉक"],
            "resolution": "Your account is locked for security. Use 'Forgot Password' or OTP from registered mobile to unlock. If failed, escalate."
        },
        "escalate_payment": {
            "keywords": ["payment failed", "refund"],
            "resolution": "Escalating your payment issue to a human agent with full context."
        }
    },
    "telecom": {
        "query_bill": {
            "keywords": ["bill", "recharge"],
            "resolution": "Check bill in MyAccount app or dial *123#. For disputes, escalate."
        }
    },
    "general": {  # Fallback mirrors for common cases
        "query_balance": {
            "keywords": ["balance", "account balance", "खाता बैलेंस"],
            "resolution": "To check your balance, log in to the app with your credentials or call support. If issues, provide account #."
        },
        "complaint_lock": {
            "keywords": ["locked", "account lock", "लॉक", "खाता लॉक"],
            "resolution": "Your account is locked for security. Use 'Forgot Password' or OTP from registered mobile to unlock. If failed, escalate."
        },
        "unknown": {
            "keywords": [],
            "resolution": "I couldn't find a quick solution. Let's escalate to a specialist."
        }
    }
}

def find_resolution(intent, user_text, industry="general"):
    """Match intent + text to KB entry."""
    kb_section = KB.get(industry, KB["general"])
    for key, entry in kb_section.items():
        if intent in key and any(kw.lower() in user_text.lower() for kw in entry["keywords"]):
            return entry["resolution"]
    return None