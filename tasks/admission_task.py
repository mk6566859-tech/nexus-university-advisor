from crewai import Task

def create_admission_task(agent, student_context, catalogue_context):
    return Task(
        description=f"""
Review this student profile and the supplied university catalogue.

STUDENT:
{student_context}

CATALOGUE:
{catalogue_context}

Return compact JSON with exactly these keys:
requirements: array of requirement objects with name, required_value, source_status
documents: array of likely required documents only when supported by the catalogue
verification_needed: array of items that cannot be confirmed from the supplied catalogue
notes: one short sentence

Do not invent university policies. Keep the response compact.
""",
        expected_output="Compact JSON containing requirements, documents, verification_needed, and notes.",
        agent=agent,
    )
