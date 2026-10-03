from crewai import Task

def create_recommendation_task(agent, student_context, eligibility_output, catalogue_context):
    return Task(
        description=f"""
Recommend programmes using ONLY the supplied student profile, eligibility checkpoint, and catalogue.

STUDENT:
{student_context}

ELIGIBILITY:
{eligibility_output}

CATALOGUE:
{catalogue_context}

Return compact JSON:
recommendations: array of up to 3 objects with programme, university, fit_reason, eligibility_note
alternatives: array of up to 2 objects with programme and why_consider
caution: one short sentence

Do not rank programmes as universally best. Do not invent programme facts.
""",
        expected_output="Compact JSON with recommendations, alternatives, and caution.",
        agent=agent,
    )
