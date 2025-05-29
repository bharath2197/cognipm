import streamlit as st
import requests
from utils.memory import load_decisions, save_decision, create_entry, load_prds, save_prd, clear_prds, clear_decisions, save_okr_analysis, load_okr_analyses, clear_okr_analyses
from datetime import datetime

# 🔗 Connect to Ollama API locally
def query_ollama(prompt, model="mistral"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["response"]

# Streamlit App Setup
st.set_page_config(page_title="Cognipm", layout="wide")
st.title("🧠 Cognipm – Cognitive Assistant for Product Managers")

# Session State Initialization
if "generated_prd" not in st.session_state:
    st.session_state["generated_prd"] = ""

# Tab Setup
tabs = st.tabs([
    "📘 Decision Logger",
    "📖 Story Intelligence",
    "🧠 Internal Coach",
    "🔍 Bias Detector",
    "📅 Release Readiness",
    "📐 Feature Validator",
    "📊 OKR Fit Analyzer",
    "📝 PRD Generator",
    "📤 Export Tools",
    "📚 PRD History",
    "📈 OKR Analysis History"
])

# 📘 Decision Logger
with tabs[0]:
    st.header("📘 Decision Logger")
    raw_text = st.text_area("Describe the decision or discussion")
    if st.button("Log Decision", key="log_decision"):
        if raw_text:
            with st.spinner("Summarizing..."):
                prompt = f"Summarize this product decision in 1–2 sentences:\n{raw_text}"
                summary = query_ollama(prompt)
                entry = create_entry(raw_text, summary)
                save_decision(entry)
                st.success("✅ Decision saved with summary!")
                st.markdown(f"**Summary:** {summary}")

    st.divider()
    st.subheader("📚 Decision History")
    history = load_decisions()
    for item in reversed(history):
        st.markdown(f"**🕒 {item['timestamp']}**")
        st.markdown(f"📝 {item['raw_text']}")
        st.markdown(f"🔍 _{item['summary']}_")
        st.markdown("---")

    if st.button("🗑️ Clear All Decision History"):
        clear_decisions()
        st.success("✅ Decision history cleared!")
        st.rerun()

# 📖 Story Intelligence
with tabs[1]:
    st.header("📖 Story Intelligence Builder")
    prd_text = st.text_area("Paste your PRD or feature spec")
    if st.button("Analyze Spec", key="analyze_spec"):
        prompt = f"""
You're a senior PM. Review this spec and provide:
- Structural improvements
- Missing info
- Suggestions to improve clarity and alignment

Spec:
{prd_text}
"""
        feedback = query_ollama(prompt)
        st.markdown("**🧠 Feedback:**")
        st.markdown(feedback)

    if st.button("Save this PRD", key="save_prd_story_intelligence"):
        save_prd(prd_text)
        st.success("✅ PRD saved to history!")

# 🧠 Internal Product Coach
with tabs[2]:
    st.header("🧠 Product Coaching")
    blocker = st.text_input("What's blocking you?")
    decision_struggle = st.text_area("Decision you're struggling with?")
    if st.button("Get Coaching", key="get_coaching"):
        prompt = f"""
You're a senior product coach. Provide advice:
Blocker: {blocker}
Struggle: {decision_struggle}
"""
        advice = query_ollama(prompt)
        st.markdown("**📌 Coaching Advice:**")
        st.markdown(advice)

# 🔍 Bias Detector
with tabs[3]:
    st.header("🔍 Bias & Framing Detector")
    bias_input = st.text_area("Paste a product spec or decision")
    if st.button("Detect Bias", key="detect_bias"):
        prompt = f"""
You are an unbiased reviewer. Identify any framing bias, confirmation bias, or emotionally loaded language in the following:
{bias_input}
"""
        result = query_ollama(prompt)
        st.markdown("**🚨 Detected Bias or Framing Issues:**")
        st.markdown(result)

# 📅 Release Readiness
with tabs[4]:
    st.header("📅 Release Readiness Check")
    release_plan = st.text_area("Paste your release plan or checklist")
    if st.button("Evaluate Readiness", key="evaluate_readiness"):
        prompt = f"""
You're a release QA advisor. Review the plan and identify gaps in:
- Test coverage
- Documentation
- Communication plan
- Rollback strategy

Plan:
{release_plan}
"""
        feedback = query_ollama(prompt)
        st.markdown("**🧪 Readiness Feedback:**")
        st.markdown(feedback)

# 📐 Feature Validator
with tabs[5]:
    st.header("📐 Feature Validator")
    feature_idea = st.text_area("Describe the feature idea")
    if st.button("Validate Feature", key="validate_feature"):
        prompt = f"""
You are a strategic PM. Assess the following feature idea for:
- Clarity
- User alignment
- Strategic value
- Engineering feasibility

Feature:
{feature_idea}
"""
        analysis = query_ollama(prompt)
        st.markdown("**🔍 Feature Validation:**")
        st.markdown(analysis)

# 📊 OKR Fit Analyzer
with tabs[6]:
    st.header("📊 OKR Fit Analyzer")
    okrs = st.text_area("Paste your current OKRs")
    proposal = st.text_area("Describe the new feature or initiative")
    if st.button("Analyze Fit", key="analyze_fit"):
        prompt = f"""
Evaluate how well this proposal aligns with the given OKRs. Be strict. Only give 9 or 10 if all key results are directly supported.

Give:
- Fit score (1–10)
- Alignment analysis
- What's missing
- Suggestions to improve fit

OKRs:
{okrs}

Proposal:
{proposal}
"""
        result = query_ollama(prompt)
        save_okr_analysis({"timestamp": str(datetime.now()), "okrs": okrs, "proposal": proposal, "result": result})
        st.markdown("**📈 OKR Fit Analysis:**")
        st.markdown(result)

# 📝 PRD Generator
with tabs[7]:
    st.header("📝 PRD Generator")
    idea = st.text_area("Describe the product idea or user problem")
    if st.button("Generate PRD", key="generate_prd"):
        prompt = f"""
Generate a structured Product Requirements Document (PRD) for the following idea. Include: Title, Problem Statement, Goals, Requirements, Metrics, Stakeholders, Timeline

Idea:
{idea}
"""
        st.session_state["generated_prd"] = query_ollama(prompt)

    if st.session_state["generated_prd"]:
        st.markdown("**📄 Generated PRD:**")
        st.markdown(st.session_state["generated_prd"])

        if st.button("Save this PRD", key="save_prd_generator"):
            save_prd(st.session_state["generated_prd"])
            st.success("✅ PRD saved to history!")

# 📤 Export Tools
with tabs[8]:
    st.header("📤 Export Tools")
    export_text = st.text_area("Paste any notes, decisions, or summaries to export")
    if st.button("Export as Markdown", key="export_md"):
        st.download_button("Download .md", data=export_text, file_name="cognipm_export.md")
    if st.button("Export as Plain Text", key="export_txt"):
        st.download_button("Download .txt", data=export_text, file_name="cognipm_export.txt")

# 📚 PRD History
with tabs[9]:
    st.header("📚 PRD History Viewer")
    prd_history = load_prds()

    search_title = st.text_input("🔍 Filter by keyword in PRD title or content")
    filter_date = st.date_input("📅 Filter by date (optional)", value=None, key="filter_date")

    for item in reversed(prd_history):
        if search_title and search_title.lower() not in item["text"].lower():
            continue
        if filter_date and filter_date.strftime("%Y-%m-%d") not in item["timestamp"]:
            continue

        st.markdown(f"**🕒 {item['timestamp']}**")
        st.markdown(f"📄 {item['text']}")
        st.markdown("---")

    if st.button("🗑️ Clear All PRD History"):
        clear_prds()
        st.success("✅ PRD history cleared!")
        st.rerun()

# 📈 OKR Analysis History
with tabs[10]:
    st.header("📈 OKR Analysis History")
    okr_analysis = load_okr_analyses()

    for item in reversed(okr_analysis):
        st.markdown(f"**🕒 {item['timestamp']}**")
        st.markdown(f"📋 **OKRs:** {item['okrs']}")
        st.markdown(f"📝 **Proposal:** {item['proposal']}")
        st.markdown(f"📈 **Analysis Result:** {item['result']}")
        st.markdown("---")

    if st.button("🗑️ Clear All OKR Analysis History"):
        clear_okr_analyses()
        st.success("✅ OKR analysis history cleared!")
        st.rerun()
