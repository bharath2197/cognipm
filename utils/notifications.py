import requests
import os
from dotenv import load_dotenv

load_dotenv()

VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
VONAGE_FROM_NUMBER = os.getenv("VONAGE_FROM_NUMBER")


def send_sms_notification(to_number, message):
    url = "https://rest.nexmo.com/sms/json"
    payload = {
        "api_key": VONAGE_API_KEY,
        "api_secret": VONAGE_API_SECRET,
        "to": to_number,
        "from": VONAGE_FROM_NUMBER,
        "text": message
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        if data["messages"][0]["status"] == "0":
            print("✅ SMS sent successfully")
        else:
            print("❌ SMS failed:", data["messages"][0]["error-text"])
    else:
        print("❌ SMS API error:", response.status_code, response.text)
