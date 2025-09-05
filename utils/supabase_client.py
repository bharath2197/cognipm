# utils/supabase_client.py
import os
from supabase_py import create_client, Client
from dotenv import load_dotenv

# Load variables from .env in the project root
load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL", "https://oyjxnjaesbapqanbluit.supabase.co")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95anhuamFlc2JhcHFhbmJsdWl0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYxNzU1MjQsImV4cCI6MjA3MTc1MTUyNH0.KQ5fp5pKVLK8TcpwYCwzX86qrX8Pmq43ymXDe_9tRno")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95anhuamFlc2JhcHFhbmJsdWl0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYxNzU1MjQsImV4cCI6MjA3MTc1MTUyNH0.KQ5fp5pKVLK8TcpwYCwzX86qrX8Pmq43ymXDe_9tRno")

# Create the anon client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Expose 'sb' for backward compatibility
sb: Client = supabase

# Create the service‑role client (bypasses RLS)
sb_service: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
