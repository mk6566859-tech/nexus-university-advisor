from crewai import Agent
from services.groq_client import build_llm

def create_recommendation_agent() -> Agent:
    return Agent(
        role="Programme Recommendation Specialist",
        goal="Identify programme options that fit the student's profile, interests, and stated target.",
        backstory=(
            "You are an academic programme advisor. Use the supplied programme catalogue and eligibility "
            "findings. Explain fit using evidence from the provided data, and distinguish suggestions from verified facts."
        ),
        llm=build_llm("recommendation"),
        allow_delegation=False,
        verbose=False,
    )
