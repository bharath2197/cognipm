import streamlit as st
from datetime import datetime
from utils.supabase_client import sb  # use sb for anon or sb_service for full access

# -----------------------------
# Supabase Helper Functions
# -----------------------------
def get_goals():
    response = sb.table("roadmap_goals").select("*").execute()
    return response.data if response.data else []

def add_goal(title, owner, tags, target_date, priority):
    sb.table("roadmap_goals").insert({
        "title": title,
        "owner": owner,
        "tags": tags,
        "target_date": target_date,
        "priority": priority,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

def delete_goal(goal_id):
    sb.table("initiatives").delete().eq("goal_id", goal_id).execute()
    sb.table("roadmap_goals").delete().eq("id", goal_id).execute()

def get_initiatives(goal_id):
    response = sb.table("initiatives").select("*").eq("goal_id", goal_id).execute()
    return response.data if response.data else []

def add_initiative_to_goal(goal_id, title):
    sb.table("initiatives").insert({
        "goal_id": goal_id,
        "title": title,
        "status": "Not Started",
        "created_at": datetime.utcnow().isoformat()
    }).execute()

def update_initiative_status(goal_id, initiative_id, new_status):
    sb.table("initiatives").update({
        "status": new_status
    }).eq("id", initiative_id).eq("goal_id", goal_id).execute()

def delete_initiative(goal_id, initiative_id):
    sb.table("initiatives").delete().eq("id", initiative_id).eq("goal_id", goal_id).execute()

# -----------------------------
# Streamlit UI Logic
# -----------------------------
def roadmap_tracker():
    st.subheader("🎯 Your Roadmap Goals")

    goals = get_goals()
    if not goals:
        st.info("No goals available. Please add one from the main dashboard.")
        return

    goal_titles = [g['title'] for g in goals]
    selected_goal_idx = st.selectbox("Select a Goal", list(range(len(goals))), format_func=lambda i: goal_titles[i])
    goal = goals[selected_goal_idx]
    goal_id = goal["id"]

    # Goal details
    st.markdown(f"""
    ### 📓 {goal['title']} ({goal['priority']})
    - **Owner**: {goal['owner']}
    - **Target Date**: {goal['target_date']}
    - **Tags**: {goal['tags']}
    """)

    if st.button("🗑️ Delete Goal"):
        if st.checkbox("I confirm deletion"):
            delete_goal(goal_id)
            st.success("🚮 Goal deleted.")
            st.experimental_rerun()

    # Load initiatives
    st.markdown("### 🚀 Initiatives")
    initiatives = get_initiatives(goal_id)
    completed_count = 0

    for initiative in initiatives:
        initiative_id = initiative["id"]
        col1, col2 = st.columns([8, 2])
        with col1:
            st.markdown(f"• **{initiative['title']}** — `{initiative['status']}`")
        with col2:
            if st.button("🗑️", key=f"del_{initiative_id}"):
                delete_initiative(goal_id, initiative_id)
                st.success("🚮 Initiative deleted.")
                st.experimental_rerun()

        new_status = st.selectbox(
            f"Update status for: {initiative['title']}",
            ["", "Not Started", "In Progress", "Completed"],
            index=0,
            key=f"status_{initiative_id}"
        )
        if st.button(f"Update Status - {initiative_id}"):
            if not new_status.strip():
                st.warning("⚠️ Please select a valid status.")
            else:
                update_initiative_status(goal_id, initiative_id, new_status)
                st.success("✅ Status updated.")
                st.experimental_rerun()

        if initiative['status'] == "Completed":
            completed_count += 1

    total = len(initiatives)
    if total > 0:
        st.progress(completed_count / total)
        st.markdown(f"**{completed_count}/{total} Initiatives Completed ({round(100 * completed_count / total)}%)**")

    # Add Initiative
    with st.expander("➕ Add Initiative"):
        new_initiative_name = st.text_input("Initiative name", key="new_initiative_name")
        if st.button("Add Initiative"):
            if not new_initiative_name.strip():
                st.warning("🚨 Initiative name cannot be empty.")
            else:
                add_initiative_to_goal(goal_id, new_initiative_name)
                st.success("✅ Initiative added!")
                st.experimental_rerun()
