
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
    TestCaseAgent,
    ArchitectureDiagramAgent,
    BusinessProcessAgent,
    AIChallengeAgent,
    TestCoverageAgent,
    RequirementCompletenessAgent,
    RequirementRefinementAgent
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
    process_agent = BusinessProcessAgent(client)
    process_flow = process_agent.generate_process_flow(
    transcript_text
    )
    st.subheader("🧠 Meeting Analysis")

    st.json(meeting_data)
    st.subheader("🔄 Business Process Flow")
    # =========================
# BUSINESS PROCESS FLOW
# =========================

process_agent = BusinessProcessAgent(client)

process_flow = process_agent.generate_process_flow(
    transcript_text
)

st.subheader(
    "🔄 Business Process Visualization"
)

steps = [
    s.strip()
    for s in process_flow.split("\n")
    if s.strip()
]

for i, step in enumerate(steps):

    st.info(
            f"📦 {step}"
    )

    if i < len(steps) - 1:
        st.markdown(
            "<h2 style='text-align:center'>⬇️</h2>",
            unsafe_allow_html=True
        )



    # =========================
    # BRD
    # =========================

    brd = generate_brd(
        str(meeting_data)
    )

    st.subheader("📄 Business Requirement Document")

    st.write(brd)

    challenge_agent = AIChallengeAgent(
    client
    )

    challenge_review = (
    challenge_agent.challenge_requirements(
    brd
    )
    )

    st.subheader(
    "🔍 AI Challenge Review"
    )

    st.write(
    challenge_review
    )

    if st.button("✨ Refine Requirements"):

        refinement_agent = RequirementRefinementAgent(
            client
        )

        refined_brd = (
            refinement_agent.refine_requirements(
                brd,
                challenge_review
            )
        )

        st.subheader(
            "✨ Refined BRD"
        )

        st.write(
            refined_brd
        )
    # =========================
# REQUIREMENT COMPLETENESS
# =========================

    completeness_agent = RequirementCompletenessAgent(
        client
    )

    completeness_review = (
        completeness_agent.assess_completeness(
            brd
        )
    )

    st.subheader(
        "📊 Requirement Completeness"
    )

    st.write(
        completeness_review
    )

    st.subheader(
        "🚦 Delivery Health Dashboard"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Requirements",
            "78%"
        )

    with col2:
        st.metric(
            "Design",
            "85%"
        )

    with col3:
        st.metric(
            "Testing",
            "72%"
        )

    with col4:
        st.metric(
            "Overall",
            "78%"
        )
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
    diagram_agent = ArchitectureDiagramAgent(
    client
    )

    diagram = diagram_agent.generate_diagram(
    requirements,
    hld
    )

    st.subheader("🏛️ Architecture Diagram")

    st.code(
    diagram,
    language="text"
    )


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

    st.subheader("🧪 Test Cases Review")

    edited_test_cases = st.text_area(
        "Review and update test cases before approval",
        value=test_cases,
        height=500
    )
    reviewer_name = st.text_input(
        "Reviewer Name"
    )

    review_comments = st.text_area(
        "Review Comments",
        height=100
    )
    
    if st.button("✅ Approve Test Cases"):

        st.session_state[
            "approved_test_cases"
        ] = edited_test_cases

        st.session_state[
            "reviewer_name"
        ] = reviewer_name

        st.session_state[
            "review_comments"
        ] = review_comments

        st.success(
            "Test Cases Approved"
        )

    if "approved_test_cases" in st.session_state:

        st.subheader(
            "📋 Approved Test Cases"
        )

        st.write(
            f"Reviewer: {st.session_state['reviewer_name']}"
        )

        st.write(
        f"Comments: {st.session_state['review_comments']}"
        )

        st.write(
            st.session_state[
                "approved_test_cases"
            ]
        )

    coverage_agent = TestCoverageAgent(
    client
    )

    coverage_review = (
    coverage_agent.review_coverage(
    brd,
    jira_output,
    edited_test_cases
    )
    )

    st.subheader(
    "📊 Test Coverage Review"
    )

    st.write(
    coverage_review
    )
    if st.button(
        "🚀 Ready For Jira"
    ):
        st.success(
        "Test Cases Reviewed and Ready For Jira"
        )


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

