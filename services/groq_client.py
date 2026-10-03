import os
from typing import Any

from crewai import LLM
from services.config import MODEL_NAME, GROQ_API_KEY_ENV, AGENT_MAX_COMPLETION


class _GroqLLM(LLM):
    def call(self, messages: Any, *args: Any, **kwargs: Any) -> Any:
        if isinstance(messages, list):
            messages = [
                {key: value for key, value in message.items() if key != "cache_breakpoint"}
                if isinstance(message, dict)
                else message
                for message in messages
            ]
        return super().call(messages, *args, **kwargs)


def build_llm(stage: str) -> LLM:
    """Create a CrewAI LLM backed by Groq's OpenAI-compatible endpoint."""
    api_key = os.getenv(GROQ_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to Streamlit Cloud → App settings → Secrets."
        )
    max_tokens = AGENT_MAX_COMPLETION.get(stage, 700)
    return _GroqLLM(
        model=f"groq/{MODEL_NAME}",
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        temperature=0.1,
        max_completion_tokens=max_tokens,
    )
