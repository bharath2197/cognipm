from google.cloud import firestore
from google.oauth2 import service_account

KEY_PATH = "C:/Users/bhara/cognipm/clean-cognipm/firebase_service_account.json"
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
db = firestore.Client(credentials=credentials, project="cognipm")

# Try to read any collection (like "users")
for doc in db.collection("users").stream():
    print(doc.id, doc.to_dict())
