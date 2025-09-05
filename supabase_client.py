# utils/supabase_client.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # loads .env in dev; harmless in prod if absent

SUPABASE_URL = os.getenv("https://oyjxnjaesbapqanbluit.supabase.co")            # <-- env VAR NAME
SUPABASE_ANON_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95anhuamFlc2JhcHFhbmJsdWl0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYxNzU1MjQsImV4cCI6MjA3MTc1MTUyNH0.KQ5fp5pKVLK8TcpwYCwzX86qrX8Pmq43ymXDe_9tRno")  # <-- env VAR NAME
SUPABASE_SERVICE_ROLE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95anhuamFlc2JhcHFhbmJsdWl0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjE3NTUyNCwiZXhwIjoyMDcxNzUxNTI0fQ.7gAK8ZX7saSdWmUGMkjIp1vMMZtzQ3-7x_FaoSULQzA")  # optional (server-only)

def _require(name: str, value: str | None):
    if not value:
        raise RuntimeError(
            f"Missing {name}. Set it in your environment or .env (e.g., {name}=...)."
        )

_require("SUPABASE_URL", SUPABASE_URL)
_require("SUPABASE_ANON_KEY", SUPABASE_ANON_KEY)

# App client (RLS enforced)
sb: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Service-role client (bypasses RLS) — use ONLY in server-side scripts/tasks
sb_service: Client | None = (
    create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    if SUPABASE_SERVICE_ROLE_KEY else None
)
