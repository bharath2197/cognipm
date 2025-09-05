import streamlit as st
from utils.agent_planner import plan_steps_from_goal
from utils.agent_executor import execute_step_chain
from utils.supabase_client import sb  # Use anon or sb_service if needed
from datetime import datetime

def run_product_agent():
    st.header("🧠 Product Goal Agent")

    username = st.session_state.get("username", "guest")
    goal = st.text_area(
        "Describe your product goal or problem:",
        placeholder="e.g., Evaluate the viability of launching Slack integration for enterprise users"
    )

    if st.button("Analyze"):
        if not goal.strip():
            st.warning("Please enter a product goal.")
            return

        with st.spinner("🧠 Thinking..."):
            steps = plan_steps_from_goal(goal)
            st.subheader("📋 Planned Steps")
            for i, step in enumerate(steps, 1):
                st.markdown(f"**Step {i}:** {step}")

            result = execute_step_chain(steps, goal, username)
            st.session_state.agent_summary = result["summary"]
            st.session_state.agent_session_id = result["session_id"]

            st.subheader("📝 Agent Summary")
            st.success(result["summary"])

    # Feedback buttons
    if "agent_summary" in st.session_state:
        st.subheader("📄 Rate this Response")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Helpful"):
                sb.table("agent_sessions").update({
                    "feedback": "up"
                }).eq("id", st.session_state.agent_session_id).execute()
                st.success("Thanks for your feedback!")
        with col2:
            if st.button("👎 Not Helpful"):
                sb.table("agent_sessions").update({
                    "feedback": "down"
                }).eq("id", st.session_state.agent_session_id).execute()
                st.info("We appreciate your honesty!")
