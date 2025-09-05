# user_auth.py

import bcrypt
from utils.supabase_client import supabase, sb_service

def add_user(username, name, email, password):
    response = supabase.table("users").select("username").eq("username", username).execute()
    if response.data:
        return False

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    sb_service.table("users").insert({
        "username": username,
        "name": name,
        "email": email,
        "password": hashed_pw
    }).execute()
    return True

def authenticate_user(username, password):
    response = supabase.table("users").select("password").eq("username", username).execute()
    if not response.data:
        return False

    stored_pw = response.data[0]["password"]
    return bcrypt.checkpw(password.encode(), stored_pw.encode())
