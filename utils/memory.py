from datetime import datetime
from supabase import create_client
import os

# 🔌 Supabase Initialization
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "your-service-role-key")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------------
# 📘 Decisions
# --------------------------
def create_entry(raw_text, summary, username):
    return {
        "timestamp": str(datetime.now()),
        "username": username,
        "raw_text": raw_text,
        "summary": summary
    }

def save_decision(entry):
    supabase.table("decisions").insert(entry).execute()

def load_decisions(username):
    response = supabase.table("decisions").select("*").eq("username", username).execute()
    return response.data

def clear_decisions(username):
    supabase.table("decisions").delete().eq("username", username).execute()

# --------------------------
# 📝 PRDs
# --------------------------
def save_prd(prd_text, username):
    supabase.table("prds").insert({
        "timestamp": str(datetime.now()),
        "username": username,
        "text": prd_text
    }).execute()

def load_prds(username):
    response = supabase.table("prds").select("*").eq("username", username).execute()
    return response.data

def clear_prds(username):
    supabase.table("prds").delete().eq("username", username).execute()

# --------------------------
# 📊 OKR Analyses
# --------------------------whats 
def save_okr_analysis(analysis_entry):
    supabase.table("okr_analyses").insert(analysis_entry).execute()

def load_okr_analyses(username):
    response = supabase.table("okr_analyses").select("*").eq("username", username).execute()
    return response.data

def clear_okr_analyses(username):
    supabase.table("okr_analyses").delete().eq("username", username).execute()

# --------------------------
# 🛂 Roadmap History
# --------------------------
def save_roadmap(roadmap_text, username):
    supabase.table("roadmaps").insert({
        "timestamp": str(datetime.now()),
        "username": username,
        "text": roadmap_text
    }).execute()

def load_roadmaps(username):
    response = supabase.table("roadmaps").select("*").eq("username", username).execute()
    return response.data

def clear_roadmaps(username):
    supabase.table("roadmaps").delete().eq("username", username).execute()

# --------------------------
# 📍 Roadmap Goals (Phase 2 Tracker)
# --------------------------
def save_roadmap_goal(goal_data):
    supabase.table("roadmap_goals").insert(goal_data).execute()

def load_roadmap_goals(username):
    response = supabase.table("roadmap_goals").select("*").eq("username", username).execute()
    return response.data
