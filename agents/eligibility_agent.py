from crewai import Agent
from services.groq_client import build_llm

def create_eligibility_agent() -> Agent:
    return Agent(
        role="Student Eligibility Evaluator",
        goal="Compare the student's profile with the supplied admission requirements and explain each match or gap.",
        backstory=(
            "You are a methodical eligibility evaluator. Separate confirmed matches, missing information, "
            "and requirements that require official verification. Never invent grades, test scores, or policies."
        ),
        llm=build_llm("eligibility"),
        allow_delegation=False,
        verbose=False,
    )
