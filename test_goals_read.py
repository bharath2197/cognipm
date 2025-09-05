from google.cloud import firestore
from google.oauth2 import service_account

KEY_PATH = "C:/Users/bhara/cognipm/clean-cognipm/firebase_service_account.json"
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
db = firestore.Client(credentials=credentials, project="cognipm-465321")

try:
    docs = db.collection("goals").stream()
    for doc in docs:
        print(doc.id, doc.to_dict())
except Exception as e:
    print("READ FAILED:", e)