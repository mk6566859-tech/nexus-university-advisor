import os

APP_NAME = "Nexus University Advisor"
MAX_TOTAL_TOKENS = 7500
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY_ENV = "GROQ_API_KEY"

# Per-agent completion ceilings. Four calls = at most 3,300 generated tokens.
AGENT_MAX_COMPLETION = {
    "admission": 700,
    "eligibility": 700,
    "recommendation": 800,
    "advisor": 1100,
}
