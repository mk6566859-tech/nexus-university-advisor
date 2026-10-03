import json
from crewai import Crew, Process

from agents.admission_agent import create_admission_agent
from agents.eligibility_agent import create_eligibility_agent
from agents.recommendation_agent import create_recommendation_agent
from agents.advisor_agent import create_advisor_agent

from tasks.admission_task import create_admission_task
from tasks.eligibility_task import create_eligibility_task
from tasks.recommendation_task import create_recommendation_task
from tasks.advisor_task import create_advisor_task

from services.token_manager import compact_json, normalize_output, clip_text, budget_snapshot, enforce_budget, enforce_stage_budget

class UniversityAdvisorCrew:
    def __init__(self):
        self.admission_agent = create_admission_agent()
        self.eligibility_agent = create_eligibility_agent()
        self.recommendation_agent = create_recommendation_agent()
        self.advisor_agent = create_advisor_agent()

    def run(self, student: dict) -> dict:
        catalogue = self._load_catalogue(student.get("university", ""), student.get("program", ""))
        student_context = compact_json(student, 1200)
        catalogue_context = compact_json(catalogue, 1600)

        admission_task = create_admission_task(
            self.admission_agent, clip_text(student_context, 1200), clip_text(catalogue_context, 1600)
        )
        enforce_stage_budget(admission_task.description, 700)
        admission_result = Crew(
            agents=[self.admission_agent],
            tasks=[admission_task],
            process=Process.sequential,
            verbose=False,
        ).kickoff()
        admission_output = normalize_output(admission_result)

        eligibility_task = create_eligibility_task(
            self.eligibility_agent, clip_text(student_context, 1200), clip_text(admission_output, 1400)
        )
        enforce_stage_budget(eligibility_task.description, 700)
        eligibility_result = Crew(
            agents=[self.eligibility_agent],
            tasks=[eligibility_task],
            process=Process.sequential,
            verbose=False,
        ).kickoff()
        eligibility_output = normalize_output(eligibility_result)

        recommendation_task = create_recommendation_task(
            self.recommendation_agent,
            clip_text(student_context, 1200),
            clip_text(eligibility_output, 1400),
            clip_text(catalogue_context, 1600),
        )
        enforce_stage_budget(recommendation_task.description, 800)
        recommendation_result = Crew(
            agents=[self.recommendation_agent],
            tasks=[recommendation_task],
            process=Process.sequential,
            verbose=False,
        ).kickoff()
        recommendation_output = normalize_output(recommendation_result)

        advisor_task = create_advisor_task(
            self.advisor_agent,
            clip_text(student_context, 1000),
            clip_text(admission_output, 550),
            clip_text(eligibility_output, 550),
            clip_text(recommendation_output, 550),
        )
        enforce_stage_budget(advisor_task.description, 1100)
        advisor_result = Crew(
            agents=[self.advisor_agent],
            tasks=[advisor_task],
            process=Process.sequential,
            verbose=False,
        ).kickoff()
        final_report = normalize_output(advisor_result)

        usage_inputs = [
            student_context, catalogue_context,
            admission_task.description, admission_output,
            eligibility_task.description, eligibility_output,
            recommendation_task.description, recommendation_output,
            advisor_task.description, final_report,
        ]
        usage = budget_snapshot(usage_inputs)
        enforce_budget(usage_inputs)

        return {
            "final_report": final_report,
            "stages": {
                "admission": admission_output,
                "eligibility": eligibility_output,
                "recommendation": recommendation_output,
            },
            "usage": usage,
        }

    @staticmethod
    def _load_catalogue(university: str, program: str):
        path = "data/universities.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Prefer exact university; otherwise provide the small demo catalogue.
        universities = [
            u for u in data.get("universities", [])
            if u.get("name", "").lower() == university.lower()
        ]
        if not universities:
            universities = data.get("universities", [])

        selected = []
        for uni in universities:
            programmes = uni.get("programmes", [])
            if program:
                matches = [
                    p for p in programmes
                    if program.lower() in p.get("name", "").lower()
                    or p.get("name", "").lower() in program.lower()
                ]
                selected.extend([{"university": uni["name"], "programme": p} for p in matches])
            else:
                selected.extend([{"university": uni["name"], "programme": p} for p in programmes[:4]])

        return {"matches": selected[:6], "catalogue_note": data.get("note", "")}
