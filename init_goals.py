from google.cloud import firestore
from google.oauth2 import service_account

KEY_PATH = "C:/Users/bhara/cognipm/clean-cognipm/firebase_service_account.json"
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
db = firestore.Client(credentials=credentials, project="cognipm-465321")

# Add a dummy document to create 'goals' collection
db.collection("goals").add({
    "title": "Initialize Collection",
    "description": "This is a dummy goal to initialize the collection",
})
print("Dummy goal added successfully.")
