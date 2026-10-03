import os
from crewai import LLM
from services.config import MODEL_NAME, GROQ_API_KEY_ENV, AGENT_MAX_COMPLETION

def build_llm(stage: str) -> LLM:
    """Create a CrewAI LLM backed by Groq's OpenAI-compatible endpoint."""
    api_key = os.getenv(GROQ_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to Streamlit Cloud → App settings → Secrets."
        )
    max_tokens = AGENT_MAX_COMPLETION.get(stage, 700)
    return LLM(
        model=f"groq/{MODEL_NAME}",
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        temperature=0.1,
        max_completion_tokens=max_tokens,
    )
