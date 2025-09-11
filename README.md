# Cognipm

**Cognipm** is an AI-powered assistant for Product Managers that helps log product decisions, align them with OKRs, and instantly generate PRDs. It integrates with LLMs and notifications (like SMS) to bring intelligent decision workflows into your product development process.

## What it does

- Logs product decisions and ties them to objectives
- Generates PRDs automatically from high-level ideas
- Sends real-time decision alerts via SMS (powered by Vonage)
- Explains decision rationale and alignment using LLM
- Includes modules like:
  - Product Coach
  - Roadmap Tracker
  - Bias Detector
  - OKR Fit Analyzer

## Tech used

- **Python** – Core logic and backend processing
- **Streamlit** – Lightweight, interactive web UI
- **Supabase** – Postgres-powered backend for memory, auth, and storage
- **Vonage SMS API** – Real-time product decision alerts via SMS
- **Incredible LLM API** – Cloud-hosted language model for product content generation
- **python-dotenv** – Secrets and environment management
- **Requests & HTTPX** – Handling external and async API calls
- **Git & GitHub** – Version control and collaboration

## To run locally

```bash
git clone https://github.com/bharath2197/cognipm.git
cd cognipm
pip install -r requirements.txt
streamlit run cognipm_dashboard.py
```

## What's next

- Integrate API-based LLMs for broader use
- Add lightweight onboarding and memory tracking
- Explore integrations with tools like Jira and Notion
- Host a live demo with mock data
- Add PDF/Doc export of PRDs and decision logs
