from crewai import Task

def create_advisor_task(agent, student_context, admission_output, eligibility_output, recommendation_output):
    return Task(
        description=f"""
Create the final student-facing advisory report from these compact checkpoints.

STUDENT:
{student_context}

ADMISSION:
{admission_output}

ELIGIBILITY:
{eligibility_output}

RECOMMENDATIONS:
{recommendation_output}

Write a concise Markdown report with these headings:
## Eligibility snapshot
## What you need
## Programme options
## Important verification
## Next 3 steps

Use only supplied evidence. Clearly label anything that needs official verification.
Do not claim that a programme or university requirement is current unless the supplied catalogue confirms it.
""",
        expected_output="Concise Markdown advisory report with five requested headings.",
        agent=agent,
    )
