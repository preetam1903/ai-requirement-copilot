
import streamlit as st

from openai import OpenAI

from audio_recorder_streamlit import audio_recorder

from agents import (
    RequirementAgent,
    HLDAgent,
    SolutionAgent,
    QueryAgent,
    InsightAgent
)


# =========================
# OPENAI CLIENT
# =========================

client = OpenAI(
    api_key="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")


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Requirement Engineering Copilot",
    layout="wide"
)

st.title("🎤 AI Requirement Engineering Copilot")

st.write(
    """
Speak your business requirement and let AI generate:

- BRD
- Requirements
- HLD
- Table Join Architecture
- Solution Design
- Python Query
- Executive Summary
"""
)


# =========================
# AUDIO RECORDER
# =========================

audio_bytes = audio_recorder()


# =========================
# AUDIO PLAYBACK
# =========================

if audio_bytes:

    st.audio(
        audio_bytes,
        format="audio/wav"
    )


# =========================
# SAVE AUDIO FILE
# =========================

if audio_bytes:

    with open("requirement.wav", "wb") as f:

        f.write(audio_bytes)


# =========================
# SPEECH TO TEXT
# =========================

if audio_bytes:

    with open("requirement.wav", "rb") as audio_file:

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    requirement_text = transcript.text

    st.subheader("📝 Requirement Transcript")

    st.write(requirement_text)


    # =========================
    # BRD GENERATION
    # =========================

    def generate_brd(requirement_text):

        prompt = f"""
        Convert the spoken requirement below
        into a professional Business Requirement Document.

        Include:
        - business objective
        - scope
        - functional requirements
        - operational requirements
        - data requirements
        - expected outcomes

        Requirement:
        {requirement_text}
        """

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an enterprise business analyst."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content


    # =========================
    # GENERATE BRD
    # =========================

    brd = generate_brd(
        requirement_text
    )

    st.subheader("📄 Generated BRD")

    st.write(brd)


    # =========================
    # REQUIREMENT AGENT
    # =========================

    requirement_agent = RequirementAgent(client)

    requirements = requirement_agent.extract_requirements(
        brd
    )

    st.subheader("📌 Extracted Requirements")

    st.write(requirements)


    # =========================
    # HLD AGENT
    # =========================

    hld_agent = HLDAgent(client)

    hld = hld_agent.generate_hld(
        requirements
    )

    st.subheader("🏗️ Generated HLD")

    st.write(hld)


    # =========================
    # TABLE RELATIONSHIP VIEW
    # =========================

    st.subheader("🔗 Manufacturing Table Join Architecture")

    st.code(
        """
PRODUCTION_DATA.MAT_ID
    ↓ joins with
DEFECT_DATA.MAT_ID

Purpose:
Identify operational defects impacting coils.


PRODUCTION_DATA.ORDER_NO
    ↓ joins with
ORDER_DATA.ORDER_NO

Purpose:
Retrieve customer and delivery details.


MATERIAL_FLOW_DATA.MAT_ID_NEXT
    ↓ joins with
PRODUCTION_DATA.MAT_ID

Purpose:
Trace parent-child coil lineage.


PRODUCTION_DATA.ROUTE
    ↓ parsed dynamically
NEXT_INSTALLATION

Purpose:
Derive next manufacturing step dynamically.
""",
        language="text"
    )


    # =========================
    # SOLUTION AGENT
    # =========================

    solution_agent = SolutionAgent(client)

    solution = solution_agent.generate_solution(
        requirements,
        hld
    )

    st.subheader("⚙️ Generated Solution")

    st.write(solution)


    # =========================
    # QUERY AGENT
    # =========================

    query_agent = QueryAgent(client)

    python_query = query_agent.generate_query(
        requirements,
        solution
    )

    st.subheader("🐍 Generated Python Query")

    st.code(
        python_query,
        language="python"
    )


    # =========================
    # EXECUTIVE SUMMARY
    # =========================

    insight_agent = InsightAgent(client)

    summary = insight_agent.generate_summary(
        requirements,
        hld,
        solution
    )

    st.subheader("📊 Executive Summary")

    st.write(summary)


# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "Enterprise Voice-enabled Agentic AI Requirement Engineering Platform"
)

