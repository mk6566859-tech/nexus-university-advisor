from crewai import Agent
from services.groq_client import build_llm

def create_admission_agent() -> Agent:
    return Agent(
        role="Admission Requirements Analyst",
        goal="Identify the relevant admission requirements for the student's target university and programme.",
        backstory=(
            "You are a careful university admissions analyst. Use only the university data supplied "
            "to you. If exact requirements are not present, clearly mark them as needing verification "
            "rather than inventing facts."
        ),
        llm=build_llm("admission"),
        allow_delegation=False,
        verbose=False,
    )
