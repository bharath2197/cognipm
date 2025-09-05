import streamlit as st
from datetime import datetime, date
import io
import csv
import pandas as pd
from utils.supabase_client import sb  # Supabase app client (RLS enforced)

def run_agent_history():
    st.header("🧠 Agent Session History")

    username = st.session_state.get("username", "guest")

    search_goal = st.text_input("🔍 Search by keyword in goal")
    filter_feedback = st.selectbox("🎯 Filter by feedback", ["All", "Helpful", "Not Helpful", "Not Rated"])
    start_date = st.date_input("📅 Start Date", value=None, key="start_date")
    end_date = st.date_input("📅 End Date", value=None, key="end_date")

    # Fetch sessions from Supabase
    response = sb.table("agent_sessions") \
        .select("*") \
        .eq("username", username) \
        .order("timestamp", desc=True) \
        .execute()

    sessions = response.data if response.data else []

    results = []

    for data in sessions:
        feedback = data.get("feedback")
        ts = datetime.fromisoformat(data['timestamp']) if isinstance(data['timestamp'], str) else data['timestamp']

        if search_goal and search_goal.lower() not in data['goal'].lower():
            continue
        if filter_feedback == "Helpful" and feedback != "up":
            continue
        if filter_feedback == "Not Helpful" and feedback != "down":
            continue
        if filter_feedback == "Not Rated" and feedback is not None:
            continue
        if start_date and ts.date() < start_date:
            continue
        if end_date and ts.date() > end_date:
            continue

        results.append(data)

    if not results:
        st.info("No matching agent sessions found.")
    else:
        for data in results:
            st.markdown(f"**🕒 {data['timestamp']}**")
            st.markdown(f"**📂 Goal:** {data['goal']}")
            st.markdown("**📝 Steps:**")
            for i, step in enumerate(data['steps'], 1):
                st.markdown(f"- Step {i}: {step}")
            st.markdown("**📈 Summary:**")
            st.markdown(data['summary'])
            feedback = data.get("feedback")
            if feedback == "up":
                st.markdown("**Feedback:** 👍 Helpful")
            elif feedback == "down":
                st.markdown("**Feedback:** 👎 Not Helpful")
            else:
                st.markdown("**Feedback:** Not rated yet")
            st.markdown("---")

        # Export formats
        export_text = "\n\n".join([
            f"Goal: {data['goal']}\nSteps: {', '.join(data['steps'])}\nSummary: {data['summary']}\nFeedback: {data.get('feedback', 'None')}\nTimestamp: {data['timestamp']}"
            for data in results
        ])
        st.download_button("📥 Export as .txt", data=export_text, file_name="agent_session_history.txt", mime="text/plain")

        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Goal", "Steps", "Summary", "Feedback", "Timestamp"])
        for data in results:
            writer.writerow([
                data['goal'], " | ".join(data['steps']), data['summary'], data.get('feedback', 'None'), data['timestamp']
            ])
        csv_string = csv_buffer.getvalue()
        st.download_button("📥 Export as .csv", data=csv_string, file_name="agent_session_history.csv", mime="text/csv")

        md_lines = [
            f"### Session - {data['timestamp']}\n"
            f"**Goal:** {data['goal']}\n\n"
            f"**Steps:**\n" + "\n".join([f"- {s}" for s in data['steps']]) + "\n\n"
            f"**Summary:**\n{data['summary']}\n\n"
            f"**Feedback:** {'👍 Helpful' if data.get('feedback') == 'up' else '👎 Not Helpful' if data.get('feedback') == 'down' else 'Not rated'}\n"
            for data in results
        ]
        md_output = "\n---\n".join(md_lines)
        st.download_button("📥 Export as .md", data=md_output, file_name="agent_session_history.md", mime="text/markdown")
