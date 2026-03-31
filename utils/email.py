import os
import requests
from dotenv import load_dotenv

# Force Python to read the .env file (for local testing)
load_dotenv()

def send_approval_email(to_email: str, name: str, temp_password: str):
    api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("BREVO_SENDER_EMAIL")
    sender_name = os.getenv("SMTP_FROM_NAME", "AgriGear ERP")

    # Debugging logs to guarantee they loaded 
    print(f"[DEBUG EMAIL] Loaded Sender Email: {sender_email}")
    print(f"[DEBUG EMAIL] API Key Loaded: {'YES' if api_key else 'NO'}")

    if not api_key or not sender_email:
        print("[ERROR] Brevo credentials are None. Check your environment variables!")
        return

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": to_email}],
        "subject": "Your AgriGear ERP Account is Approved!",
        "textContent": f"Hello {name},\n\nYour account has been approved by the Admin.\n\nYour temporary password is: {temp_password}\n\nPlease log in and change your password."
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"[EMAIL SUCCESS] Sent to {to_email} via Brevo API")
    except Exception as e:
        print(f"[EMAIL FAILED] {e}")