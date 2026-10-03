from crewai import Agent
from services.groq_client import build_llm

def create_advisor_agent() -> Agent:
    return Agent(
        role="Senior University Advisor",
        goal="Turn the three specialist checkpoints into a concise, actionable student advisory report.",
        backstory=(
            "You are the final academic advisor. You synthesize structured findings without adding unsupported "
            "facts. Be transparent about uncertainty and finish with concrete next steps."
        ),
        llm=build_llm("advisor"),
        allow_delegation=False,
        verbose=False,
    )
