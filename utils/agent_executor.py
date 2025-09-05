import datetime
import streamlit as st
from utils.supabase_client import sb_service  # Ensure sb_service is initialized

# Simulated execution logic
def simulate_step_execution(step):
    if "OKR" in step or "objective" in step.lower():
        return "✅ OKR fit validated."
    elif "risk" in step.lower():
        return "✅ Risks assessed and documented."
    elif "PRD" in step:
        return "✅ PRD drafted."
    elif "feasibility" in step or "integration" in step:
        return "✅ Technical feasibility confirmed."
    else:
        return "✅ Step completed."

def execute_step_chain(steps, goal, username):
    log = []
    for i, step in enumerate(steps, 1):
        result = simulate_step_execution(step)
        log.append(f"{i}. {step} → {result}")

    summary = "The agent completed the following:\n\n" + "\n".join(log)

    # Save to Supabase (agent_sessions table)
    try:
        result = sb_service.table("agent_sessions").insert({
            "username": username,
            "goal": goal,
            "steps": steps,
            "summary": summary,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "feedback": None
        }).execute()

        session_id = result.data[0]["id"] if result.data else None

    except Exception as e:
        st.error(f"❌ Failed to save agent session: {e}")
        session_id = None

    return {"summary": summary, "session_id": session_id}
