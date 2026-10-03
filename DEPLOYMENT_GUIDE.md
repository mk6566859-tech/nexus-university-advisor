# Beginner Deployment Guide

## Part 1 — Get the project

You received this ZIP. Extract it on your computer if you want to inspect it. You do not need to install Python, Streamlit, CrewAI, or Groq locally for the GitHub → Streamlit Cloud workflow.

## Part 2 — Create GitHub repository

1. Sign in to GitHub.
2. Click **New repository**.
3. Name it something like `nexus-university-advisor`.
4. Create the repository.
5. Upload all files and folders from this project.
6. Make sure `app.py` is at the repository root.

Do NOT upload `.streamlit/secrets.toml`. Only upload `.streamlit/secrets.toml.example`.

## Part 3 — Get a Groq API key

1. Open the Groq Console.
2. Create an API key.
3. Copy it somewhere safe.
4. Never paste it into Python source code.
5. Never commit it to GitHub.

## Part 4 — Deploy to Streamlit Community Cloud

1. Open Streamlit Community Cloud.
2. Connect your GitHub account.
3. Choose **Create app**.
4. Select your GitHub repository.
5. Branch: `main`.
6. Main file path: `app.py`.
7. Open **Advanced settings**.
8. Choose Python 3.12 if the UI asks for a Python version.
9. In **Secrets**, paste:

GROQ_API_KEY = "your_real_key"
GROQ_MODEL = "llama-3.3-70b-versatile"

10. Click Save / Deploy.
11. Wait for the build to finish.
12. Open the Streamlit URL.

## Part 5 — First test

Use the demo university:

University: Example University
Programme: BS Computer Science
Qualification: Intermediate
Grade: 82%
Subjects: Mathematics, Physics, Computer Science

The app should execute the four stages and show the final advisor report.

## Part 6 — Replace demo data

Before using the app for real students:

1. Open `data/universities.json`.
2. Replace the demo university with verified information.
3. Keep requirements tied to official sources in your own data pipeline.
4. Add a source URL field if you extend the schema.
5. Make the UI clearly state that the official university remains authoritative.

## Token budget

The code:
- limits each stage's completion length;
- caps each agent prompt at about 700 estimated input tokens;
- passes compact context instead of full conversation history;
- reserves framework overhead;
- stops the run if a stage prompt exceeds its input envelope or the final aggregate estimate exceeds 7,500 tokens.

The 7,500 number is an application guardrail, not a guarantee of the exact provider billing count. Provider tokenization/hidden reasoning can differ.

## If deployment fails

Open the Streamlit app → Manage app → Logs.

Common causes:
- missing `GROQ_API_KEY`;
- wrong Python/package version;
- malformed JSON in `data/universities.json`;
- accidentally committed secrets;
- unsupported/changed model ID.

The `requirements.txt` file is intentionally small. Streamlit Cloud installs the listed Python dependencies during deployment.
