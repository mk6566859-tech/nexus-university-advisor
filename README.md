# Nexus University Advisor

A clean, modular Streamlit + CrewAI + Groq multi-agent university advisor.

## Workflow

Student Input
→ Admission Agent
→ Eligibility Agent
→ Recommendation Agent
→ Final Advisor

The workflow is designed with a 7,500-token application budget and compact stage-to-stage context.

## Important

`data/universities.json` contains DEMO DATA ONLY. For real admissions use, replace it with verified requirements from official university sources.

## Deployment

1. Create a GitHub repository.
2. Upload this project.
3. Open Streamlit Community Cloud.
4. Create an app from `app.py`.
5. In Advanced settings → Secrets, add:
   `GROQ_API_KEY = "..."` 
   `GROQ_MODEL = "llama-3.3-70b-versatile"`
6. Deploy.

No API key belongs in GitHub.

## Verified dependency baseline

This package set was checked against the current PyPI releases available on 2026-10-03: Streamlit 1.64.0 and CrewAI 1.15.23. CrewAI's Groq integration uses the `groq/...` model prefix; the default model here is `llama-3.3-70b-versatile`.
