import json

import streamlit as st
from crew.university_crew import UniversityAdvisorCrew
from services.config import APP_NAME, MAX_TOTAL_TOKENS


def _parse_checkpoint(payload):
    if isinstance(payload, dict):
        return payload
    if not isinstance(payload, str):
        return None

    text = payload.strip()
    lines = text.splitlines()
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        checkpoint = json.loads(text)
    except json.JSONDecodeError:
        return None
    return checkpoint if isinstance(checkpoint, dict) else None


def _render_checkpoint(stage_name, payload):
    checkpoint = _parse_checkpoint(payload)
    if checkpoint is None:
        st.markdown(str(payload))
        return

    if stage_name == "admission":
        requirements = checkpoint.get("requirements", [])
        if requirements:
            st.markdown("**Entry requirements**")
            for requirement in requirements:
                with st.container(border=True):
                    st.markdown(f"**{requirement.get('name', 'Requirement')}**")
                    st.write(f"Expected: {requirement.get('required_value', 'Not listed')}")
                    source_status = requirement.get("source_status")
                    if source_status:
                        st.caption(f"Catalogue label: {source_status.replace('_', ' ').title()}")

        documents = checkpoint.get("documents", [])
        if documents:
            st.markdown("**Documents to prepare**")
            for document in documents:
                st.markdown(f"- {document}")

        if checkpoint.get("notes"):
            st.write(checkpoint["notes"])

        verification = checkpoint.get("verification_needed", [])
        if verification:
            st.warning("**Before applying**\n\n" + "\n".join(f"- {item}" for item in verification))

    elif stage_name == "eligibility":
        status = checkpoint.get("status", "not assessed").replace("_", " ").capitalize()
        st.info(f"Assessment: {status} based on the supplied catalogue.")
        if checkpoint.get("summary"):
            st.write(checkpoint["summary"])

        matches = checkpoint.get("matches", [])
        if matches:
            st.markdown("**What matches your profile**")
            for match in matches:
                st.markdown(f"- {match}")

        gaps = checkpoint.get("gaps", [])
        if gaps:
            st.markdown("**Items to check**")
            for gap in gaps:
                st.markdown(f"- {gap}")
        else:
            st.caption("No gaps identified in the supplied catalogue.")

        verification = checkpoint.get("verification_needed", [])
        if verification:
            st.warning("**Verify with the university**\n\n" + "\n".join(f"- {item}" for item in verification))

    elif stage_name == "recommendation":
        recommendations = checkpoint.get("recommendations", [])
        for recommendation in recommendations:
            with st.container(border=True):
                st.markdown(f"#### {recommendation.get('programme', 'Programme')}")
                university = recommendation.get("university")
                if university:
                    st.caption(university)
                if recommendation.get("fit_reason"):
                    st.markdown("**Why it may fit**")
                    st.write(recommendation["fit_reason"])
                if recommendation.get("eligibility_note"):
                    st.markdown("**Eligibility**")
                    st.write(recommendation["eligibility_note"])

        alternatives = checkpoint.get("alternatives", [])
        if alternatives:
            st.markdown("**Other options**")
            for alternative in alternatives:
                if isinstance(alternative, dict):
                    st.write(" · ".join(str(value) for value in alternative.values()))
                else:
                    st.markdown(f"- {alternative}")
        else:
            st.caption("No alternative programmes were found in the supplied catalogue.")

        if checkpoint.get("caution"):
            st.warning(checkpoint["caution"])

    else:
        for key, value in checkpoint.items():
            st.markdown(f"**{key.replace('_', ' ').title()}**")
            if isinstance(value, list):
                for item in value:
                    st.markdown(f"- {item}")
            else:
                st.write(value)


st.set_page_config(
    page_title=APP_NAME,
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
  --ink:#080908;
  --panel:#10120f;
  --panel2:#151813;
  --line:#2a3023;
  --lime:#d7ff3f;
  --muted:#9ca496;
  --white:#f4f6ef;
}
.stApp { background: radial-gradient(circle at 8% 8%, rgba(215,255,63,.08), transparent 28%), var(--ink); color:var(--white); }
[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:1180px; padding-top:2.2rem; padding-bottom:4rem; }
h1,h2,h3 { font-family:'Playfair Display', Georgia, serif !important; letter-spacing:-.02em; }
p, label, .stMarkdown, .stTextInput, .stSelectbox, .stNumberInput { font-family:'DM Mono', monospace; }
.hero {
  border:1px solid var(--line); border-radius:28px; padding:38px 42px;
  background:linear-gradient(135deg, rgba(35,42,28,.9), rgba(10,12,10,.96));
  box-shadow:0 0 80px rgba(215,255,63,.05);
}
.eyebrow { color:var(--lime); font:500 12px 'DM Mono',monospace; letter-spacing:.16em; text-transform:uppercase; }
.hero-title { font:600 clamp(44px,7vw,82px) 'Playfair Display',Georgia,serif; line-height:.94; margin:12px 0 16px; }
.hero-copy { max-width:720px; color:#b5bbae; font:400 14px/1.8 'DM Mono',monospace; }
.pill { display:inline-block; border:1px solid #596244; border-radius:999px; padding:7px 12px; color:var(--lime); font:500 11px 'DM Mono',monospace; margin:5px 5px 0 0; }
.step-row { display:grid; grid-template-columns:repeat(5,1fr); gap:8px; margin:22px 0 10px; }
.step { min-height:88px; border:1px solid var(--line); border-radius:16px; padding:14px; background:#0d0f0c; }
.step.active { border-color:var(--lime); box-shadow:inset 0 0 0 1px rgba(215,255,63,.15); }
.step-no { color:var(--lime); font:500 10px 'DM Mono',monospace; }
.step-name { margin-top:9px; font:500 12px 'DM Mono',monospace; color:#e9eee2; }
.section { margin-top:34px; }
.card {
  border:1px solid var(--line); border-radius:22px; padding:22px;
  background:linear-gradient(180deg, rgba(21,24,19,.96), rgba(12,14,12,.96));
}
[data-testid="stForm"] { border:1px solid var(--line); border-radius:22px; background:#0d0f0c; padding:18px; }
.stButton>button {
  background:var(--lime) !important; color:#0a0c08 !important; border:0 !important;
  border-radius:999px !important; font:500 12px 'DM Mono',monospace !important;
  padding:.72rem 1.4rem !important;
}
.stTextInput input, .stNumberInput input, .stTextArea textarea {
  background:#0a0c0a !important; color:#f3f5ed !important; border:1px solid #30372b !important;
  border-radius:12px !important; font-family:'DM Mono',monospace !important;
}
.stSelectbox div[data-baseweb="select"] > div {
  background:#0a0c0a !important; border:1px solid #30372b !important; border-radius:12px !important;
}
.metric {
  border:1px solid var(--line); border-radius:18px; padding:16px; background:#0d0f0c;
}
.metric-value { font:600 30px 'Playfair Display',serif; color:var(--lime); }
.metric-label { color:var(--muted); font:400 10px 'DM Mono',monospace; text-transform:uppercase; letter-spacing:.08em; }
.agent-chip { display:inline-block; border:1px solid #3c4530; border-radius:999px; padding:5px 9px; margin:3px; font:400 10px 'DM Mono',monospace; color:#cbd2c1; }
.small { color:var(--muted); font:400 11px/1.7 'DM Mono',monospace; }
hr { border-color:var(--line); }
@media (max-width: 800px) { .step-row { grid-template-columns:1fr 1fr; } .hero { padding:28px 22px; } }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">
  <div class="eyebrow">NEXUS / UNIVERSITY ADVISOR</div>
  <div class="hero-title">Your next<br><span style="color:#d7ff3f">academic move.</span></div>
  <div class="hero-copy">
    A four-agent CrewAI workflow that checks admission requirements, evaluates eligibility,
    recommends programmes, and turns the findings into one clear advisor report.
  </div>
  <div style="margin-top:18px">
    <span class="pill">GROQ POWERED</span>
    <span class="pill">CREWAI ONLY</span>
    <span class="pill">≤ {MAX_TOTAL_TOKENS:,} TOKENS / RUN</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="step-row">
  <div class="step active"><div class="step-no">01 / INPUT</div><div class="step-name">Student profile</div></div>
  <div class="step"><div class="step-no">02 / CHECK</div><div class="step-name">Admission agent</div></div>
  <div class="step"><div class="step-no">03 / VERIFY</div><div class="step-name">Eligibility agent</div></div>
  <div class="step"><div class="step-no">04 / MATCH</div><div class="step-name">Recommendation agent</div></div>
  <div class="step"><div class="step-no">05 / GUIDE</div><div class="step-name">Final advisor</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section"><div class="eyebrow">01 — STUDENT INPUT</div></div>', unsafe_allow_html=True)

with st.form("student_form"):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Student name", placeholder="e.g. Ayesha Khan")
        country = st.text_input("Country / education system", placeholder="e.g. Pakistan")
        qualification = st.text_input("Current qualification", placeholder="e.g. Intermediate / A-Levels")
        grade = st.text_input("Overall grade / percentage", placeholder="e.g. 82%")
    with c2:
        university = st.text_input("Target university", placeholder="e.g. Example University")
        program = st.text_input("Target programme", placeholder="e.g. Computer Science")
        subjects = st.text_input("Relevant subjects", placeholder="e.g. Mathematics, Physics, Computer Science")
        interests = st.text_input("Interests / career goals", placeholder="e.g. AI, software engineering")
    notes = st.text_area("Additional context", placeholder="Tests, gap year, diploma, preferences, budget, campus preference, etc.", height=100)
    submitted = st.form_submit_button("Run academic advisor  →", use_container_width=True)

if submitted:
    required = [name, country, qualification, grade, university, program]
    if not all(x.strip() for x in required):
        st.error("Please complete the required student and programme fields.")
        st.stop()

    student = {
        "name": name.strip(),
        "country": country.strip(),
        "qualification": qualification.strip(),
        "grade": grade.strip(),
        "university": university.strip(),
        "program": program.strip(),
        "subjects": subjects.strip(),
        "interests": interests.strip(),
        "notes": notes.strip(),
    }

    with st.status("Running the university advisor crew…", expanded=True) as status:
        st.write("Admission agent → checking requirements")
        try:
            result = UniversityAdvisorCrew().run(student)
            status.update(label="Advisor report ready", state="complete", expanded=False)
        except Exception as exc:
            status.update(label="Run failed", state="error", expanded=True)
            st.exception(exc)
            st.stop()

    st.markdown('<div class="section"><div class="eyebrow">05 — FINAL ADVISOR</div></div>', unsafe_allow_html=True)
    metrics = st.columns(3)
    with metrics[0]:
        st.markdown(f'<div class="metric"><div class="metric-value">{result["usage"]["estimated_total_tokens"]:,}</div><div class="metric-label">estimated run tokens</div></div>', unsafe_allow_html=True)
    with metrics[1]:
        st.markdown(f'<div class="metric"><div class="metric-value">{result["usage"]["budget"]:,}</div><div class="metric-label">hard workflow budget</div></div>', unsafe_allow_html=True)
    with metrics[2]:
        st.markdown(f'<div class="metric"><div class="metric-value">{len(result["stages"])}</div><div class="metric-label">agent stages</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top:16px">', unsafe_allow_html=True)
    st.markdown(result["final_report"])
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Assessment details"):
        stages = list(result["stages"].items())
        tab_labels = {
            "admission": "Requirements",
            "eligibility": "Eligibility",
            "recommendation": "Recommendations",
        }
        tabs = st.tabs([tab_labels.get(stage, stage.title()) for stage, _ in stages])
        for tab, (stage_name, payload) in zip(tabs, stages):
            with tab:
                _render_checkpoint(stage_name, payload)
else:
    st.markdown("""
    <div class="section card">
      <div class="eyebrow">HOW IT WORKS</div>
      <h2 style="font-size:32px">One profile. Four specialists.</h2>
      <p class="small">
        Your profile enters a sequential CrewAI workflow. Each specialist receives only the compact
        information it needs, reducing context duplication and keeping the run inside the token budget.
      </p>
      <div style="margin-top:12px">
        <span class="agent-chip">ADMISSION REQUIREMENTS</span>
        <span class="agent-chip">ELIGIBILITY</span>
        <span class="agent-chip">PROGRAMME MATCHING</span>
        <span class="agent-chip">FINAL ADVISOR</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
