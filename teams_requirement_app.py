
import streamlit as st

from openai import OpenAI

from docx import Document

from agents import (
    RequirementAgent,
    HLDAgent,
    SolutionAgent,
    InsightAgent,
    MeetingAgent,
    JiraAgent,
    TestCaseAgent
)

# =========================
# OPENAI CLIENT
# =========================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Meeting Requirement Copilot",
    layout="wide"
)

st.title("📋 AI Meeting Requirement Copilot")

st.write(
    """
Upload a Teams Transcript and generate:

✅ Meeting Analysis

✅ BRD

✅ Requirements

✅ HLD

✅ Solution Design

✅ Jira Stories

✅ Test Cases

✅ Executive Summary
"""
)

st.divider()

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload Teams Transcript",
    type=["txt", "docx"]
)

# =========================
# BRD GENERATOR
# =========================

def generate_brd(requirement_text):

    prompt = f"""
Convert the meeting information below
into a professional Business Requirement Document.

Include:

- Executive Summary
- Business Objective
- Scope
- Functional Requirements
- Non Functional Requirements
- Operational Requirements
- Data Requirements
- Risks
- Assumptions
- Expected Outcomes

Meeting Information:

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
# PROCESS FILE
# =========================

if uploaded_file:

    if uploaded_file.name.endswith(".txt"):

        transcript_text = (
            uploaded_file.read()
            .decode("utf-8")
        )

    else:

        doc = Document(uploaded_file)

        transcript_text = "\n".join(
            [p.text for p in doc.paragraphs]
        )

    st.subheader("📝 Teams Transcript")

    with st.expander("View Transcript"):

        st.write(transcript_text)

    # =========================
    # MEETING AGENT
    # =========================

    meeting_agent = MeetingAgent(client)

    meeting_data = (
        meeting_agent.process_transcript(
            transcript_text
        )
    )

    st.subheader("🧠 Meeting Analysis")

    st.json(meeting_data)

    # =========================
    # BRD
    # =========================

    brd = generate_brd(
        str(meeting_data)
    )

    st.subheader("📄 Business Requirement Document")

    st.write(brd)

    # =========================
    # REQUIREMENTS
    # =========================

    requirement_agent = RequirementAgent(
        client
    )

    requirements = (
        requirement_agent.extract_requirements(
            brd
        )
    )

    st.subheader("📌 Requirements")

    st.write(requirements)

    # =========================
    # HLD
    # =========================

    hld_agent = HLDAgent(client)

    hld = hld_agent.generate_hld(
        requirements
    )

    st.subheader("🏗️ High Level Design")

    st.write(hld)

    # =========================
    # SOLUTION
    # =========================

    solution_agent = SolutionAgent(
        client
    )

    solution = (
        solution_agent.generate_solution(
            requirements,
            hld
        )
    )

    st.subheader("⚙️ Solution Design")

    st.write(solution)

    # =========================
    # JIRA
    # =========================

    jira_agent = JiraAgent(client)

    jira_output = (
        jira_agent.generate_jira(
            requirements
        )
    )

    st.subheader("📋 Jira Stories")

    st.write(jira_output)

    # =========================
    # TEST CASES
    # =========================

    testcase_agent = TestCaseAgent(
        client
    )

    test_cases = (
        testcase_agent.generate_test_cases(
            jira_output
        )
    )

    st.subheader("🧪 Test Cases")

    st.write(test_cases)

    # =========================
    # EXECUTIVE SUMMARY
    # =========================

    insight_agent = InsightAgent(
        client
    )

    executive_summary = (
        insight_agent.generate_summary(
            requirements,
            hld,
            solution
        )
    )

    st.subheader("📊 Executive Summary")

    st.write(executive_summary)

    # =========================
    # DOWNLOADS
    # =========================

    st.divider()

    st.download_button(
        "Download BRD",
        brd,
        file_name="BRD.txt"
    )

    st.download_button(
        "Download Requirements",
        requirements,
        file_name="Requirements.txt"
    )

    st.download_button(
        "Download HLD",
        hld,
        file_name="HLD.txt"
    )

    st.download_button(
        "Download Solution",
        solution,
        file_name="Solution.txt"
    )

    st.download_button(
        "Download Jira Stories",
        jira_output,
        file_name="Jira_Stories.txt"
    )

    st.download_button(
        "Download Test Cases",
        test_cases,
        file_name="Test_Cases.txt"
    )

    st.download_button(
        "Download Executive Summary",
        executive_summary,
        file_name="Executive_Summary.txt"
    )

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "Enterprise AI Meeting Requirement Copilot"
)

