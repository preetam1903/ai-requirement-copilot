
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
  
    dashboard_placeholder = st.empty()
    with dashboard_placeholder.container():
        st.subheader(
            "📈 Business Impact Dashboard"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Hours Saved",
            "24"
        )

        col2.metric(
            "Cost Saved",
            "₹36K"
        )

        col3.metric(
            "Risk Reduction",
            "High"
        )

        col4.metric(
            "Readiness",
            "0%"
        )
        st.subheader(
            "📊 Executive Dashboard"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Requirements",
            "⏳"
        )

        col2.metric(
            "Jira Stories",
            "⏳"
        )

        col3.metric(
            "Test Cases",
            "⏳"
        )

        col4.metric(
            "Status",
            "Processing"
        )
        st.subheader(
            "🚦 Delivery Health"
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
    process_agent = BusinessProcessAgent(client)
    process_flow = process_agent.generate_process_flow(
    transcript_text
    )
    # =========================
# CURRENT STAGE TRACKER
# =========================

    st.subheader(
        "📍 Current Stage Tracker"
    )

    st.info(
        """
        ✅ Teams Transcript Processed

        ✅ Draft BRD Generated

        ✅ AI Challenge Review Completed

        🟡 Stakeholder Review Pending

        ⚪ Approval Pending

        ⚪ Jira Creation Pending
        """
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


    steps = process_flow.splitlines()

    steps = [
        step.strip()
        for step in steps
        if step.strip()
    ]

    for i, step in enumerate(process_flow.splitlines()):

        if step.strip():

            st.markdown(
                f"**📦 {step.strip()}**"
            )

            if i < len(process_flow.splitlines()) - 1:

                st.markdown(
                    "<div style='text-align:left;'>↓</div>",
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

    edited_challenge_review = st.text_area(
        "Review and update challenge findings",
        value=challenge_review,
        height=300
    )

    challenge_reviewer = st.text_input(
        "Challenge Reviewer"
    )

    challenge_comments = st.text_area(
        "Challenge Review Comments",
        height=100
    )

    if st.button(
        "✅ Approve Challenge Review"
    ):

        st.session_state[
            "approved_challenge_review"
        ] = edited_challenge_review

        st.session_state[
            "challenge_reviewer"
        ] = challenge_reviewer

        st.session_state[
            "challenge_comments"
        ] = challenge_comments

        st.success(
            "Challenge Review Approved"
        )

    if "approved_challenge_review" in st.session_state:

        st.subheader(
            "📋 Approved Challenge Review"
        )

        st.write(
            f"Reviewer: {st.session_state['challenge_reviewer']}"
        )

        st.write(
            f"Comments: {st.session_state['challenge_comments']}"
        )

        st.write(
            st.session_state[
                "approved_challenge_review"
            ]
        )

    if st.button("✨ Refine Requirements"):

        refinement_agent = RequirementRefinementAgent(
            client
        )

        refined_brd = (
            refinement_agent.refine_requirements(
                brd,
                st.session_stage.get(
                    "approved_challenge_review",
                challenge_review
                )   
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
    with dashboard_placeholder.container():
        st.subheader(
            "📈 Business Impact Dashboard"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Hours Saved",
            "8"
        )

        col2.metric(
            "Cost Saved",
            "₹12K"
        )

        col3.metric(
            "Risk Reduction",
            "Medium"
        )

        col4.metric(
            "Readiness",
            "25%"
        )
        
        st.subheader(
            "📊 Executive Dashboard"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Requirements",
            len(requirements.split("\n"))
        )

        col2.metric(
            "Jira Stories",
            "⏳"
        )

        col3.metric(
            "Test Cases",
            "⏳"
        )

        col4.metric(
            "Status",
            "Requirements Ready"
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
    with dashboard_placeholder.container():
        st.subheader(
            "📈 Business Impact Dashboard"
        )
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(
            "Hours Saved",
            "12"
        )

        col2.metric(
            "Cost Saved",
            "₹18K"
        )

        col3.metric(
            "Risk Reduction",
            "Medium"
        )

        col4.metric(
            "Readiness",
            "60%"
        )
        st.subheader(
            "📊 Executive Dashboard"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Requirements",
            len(requirements.split("\n"))
        )

        col2.metric(
            "Jira Stories",
            len(jira_output.split("\n"))
        )

        col3.metric(
            "Test Cases",
            "⏳"
        )

        col4.metric(
            "Status",
            "Jira Ready"
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

    with dashboard_placeholder.container():
        st.subheader(
            "📈 Business Impact Dashboard"
        )
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(
            "Hours Saved",
            "24"
        )

        col2.metric(
            "Cost Saved",
            "₹36K"
        )

        col3.metric(
            "Risk Reduction",
            "High"
        )

        col4.metric(
            "Readiness",
            "85%"
        )
        st.subheader(
            "📊 Executive Dashboard"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Requirements",
            len(requirements.split("\n"))
        )

        col2.metric(
            "Jira Stories",
            len(jira_output.split("\n"))
        )

        col3.metric(
            "Test Cases",
            len(test_cases.split("\n"))
        )

        col4.metric(
            "Status",
            "QA Ready"
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

    st.subheader(
        "🚀 Delivery Status"
    )

    delivery_status = st.selectbox(
        "Current Status",
        [

            "Draft",
            "Reviewed",
            "Approved",
            "Ready For Jira"
        ]
    )

    if delivery_status == "Draft":

        st.warning(
            "Draft in Progress"
        )

    elif delivery_status == "Reviewed":

        st.info(
            "Review Completed"
        )

    elif delivery_status == "Approved":

        st.success(
            "Approved by Reviewer"
        )

    elif delivery_status == "Ready For Jira":

        st.success(
            "Ready For Jira Deployment"
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
# EXECUTIVE DASHBOARD
# =========================


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

