from crewai import Task

def create_eligibility_task(agent, student_context, admission_output):
    return Task(
        description=f"""
Evaluate the student's eligibility using ONLY the student profile and admission checkpoint.

STUDENT:
{student_context}

ADMISSION CHECKPOINT:
{admission_output}

Return compact JSON:
status: one of eligible, potentially_eligible, not_verified
matches: array of short evidence strings
gaps: array of missing/failed requirements
verification_needed: array of items requiring official confirmation
summary: one short sentence

Do not guess missing data.
""",
        expected_output="Compact JSON with status, matches, gaps, verification_needed, and summary.",
        agent=agent,
    )
