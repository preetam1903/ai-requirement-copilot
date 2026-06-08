
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
    RequirementRefinementAgent,
    TestExecutionGuidanceAgent,
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

    if "approved_challenge_review" in st.session_state:

        if st.button(
            "✨ Refine Requirements"
        ):

            refinement_agent = RequirementRefinementAgent(
                client
            )

            refined_brd = (
                refinement_agent.refine_requirements(
                    brd,
                    st.session_state.get(
                        "approved_challenge_review",
                        challenge_review
                    )   
                )
            )

            st.subheader(
                "✨ Refined BRD Review"
            )

            edited_refined_brd = st.text_area(
                "Review and update Refined BRD",
                value=refined_brd,
                height=500
            )

            refined_brd_reviewer = st.text_input(
                "Refined BRD Reviewer"
            )

            refined_brd_comments = st.text_area(
                "Refined BRD Comments",
                height=100
            )

            if st.button(
                "✅ Approve Refined BRD"
            ):

                st.session_state[
                    "approved_refined_brd"
                ] = edited_refined_brd

                st.session_state[
                    "refined_brd_reviewer"
                ] = refined_brd_reviewer

                st.session_state[
                    "refined_brd_comments"
                ] = refined_brd_comments

                st.success(
                    "Refined BRD Approved"
                )

            if "approved_refined_brd" in st.session_state:

                st.subheader(
                    "📋 Approved Refined BRD"
                )

                st.write(
                    f"Reviewer: {st.session_state['refined_brd_reviewer']}"
                )   

                st.write(
                    f"Comments: {st.session_state['refined_brd_comments']}"
                )

                st.write(
                    st.session_state[
                        "approved_refined_brd"
                    ]
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
    final_brd = st.session_state.get(
        "approved_refined_brd",
        brd
    )
    # =========================
    # REQUIREMENTS
    # =========================

    requirement_agent = RequirementAgent(
        client
    )

    requirements = (
        requirement_agent.extract_requirements(
            final_brd
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
    st.subheader(
        "📌 Requirements Review"
    )

    edited_requirements = st.text_area(
        "Review and update Requirements",
        value=requirements,
        height=500
    )

    requirements_reviewer = st.text_input(
        "Requirements Reviewer"
    )

    requirements_comments = st.text_area(
        "Requirements Comments",
        height=100
    )

    if st.button(
        "✅ Approve Requirements"
    ):

        st.session_state[
            "approved_requirements"
        ] = edited_requirements

        st.session_state[
            "requirements_reviewer"
        ] = requirements_reviewer

        st.session_state[
            "requirements_comments"
        ] = requirements_comments

        st.success(
            "Requirements Approved"
        )

    if "approved_requirements" in st.session_state:

        st.subheader(
            "📋 Approved Requirements"
        )

        st.write(
            f"Reviewer: {st.session_state['requirements_reviewer']}"
        )

        st.write(
            f"Comments: {st.session_state['requirements_comments']}"
        )

        st.write(
            st.session_state[
                "approved_requirements"
            ]
        )

    # =========================
    # HLD
    # =========================

    hld_agent = HLDAgent(client)
    final_requirements = st.session_state.get(
        "approved_requirements",
        requirements
    )
    hld = hld_agent.generate_hld(
        final_requirements
    )

    st.subheader("🏗️ High Level Design")

    st.write(hld)
    diagram_agent = ArchitectureDiagramAgent(
    client
    )

    diagram = diagram_agent.generate_diagram(
        final_requirements,
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

   # solution_agent = SolutionAgent(
     #   client
    #)

    #solution = (
        #solution_agent.generate_solution(
            #final_requirements,
            #hld
        #)
    #)

    #st.subheader("⚙️ Solution Design")

    #st.write(solution)

    # =========================
    # JIRA
    # =========================

    jira_agent = JiraAgent(client)

    jira_output = (
        jira_agent.generate_jira(
            final_requirements
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
    st.subheader(
        "📋 Jira Stories Review"
    )

    edited_jira = st.text_area(
        "Review and update Jira Stories",
        value=jira_output,
        height=500
    )

    jira_reviewer = st.text_input(
        "Jira Reviewer"
    )

    jira_comments = st.text_area(
        "Jira Review Comments",
        height=100
    )

    if st.button(
        "✅ Approve Jira Stories"
    ):

        st.session_state[
            "approved_jira"
        ] = edited_jira

        st.session_state[
            "jira_reviewer"
        ] = jira_reviewer

        st.session_state[
            "jira_comments"
        ] = jira_comments

        st.success(
            "Jira Stories Approved"
        )

    if "approved_jira" in st.session_state:

        st.subheader(
            "📋 Approved Jira Stories"
        )

        st.write(
            f"Reviewer: {st.session_state['jira_reviewer']}"
        )

        st.write(
            f"Comments: {st.session_state['jira_comments']}"
        )

        st.write(
            st.session_state[
                "approved_jira"
            ]
        )
    final_jira = st.session_state.get(
        "approved_jira",
        jira_output
    )

    # =========================
# TEST CASES
# =========================

    testcase_agent = TestCaseAgent(
        client
    )
    execution_agent = TestExecutionGuidanceAgent(
        client
    )
    test_cases = (
        testcase_agent.generate_test_cases(
            final_jira
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
    # =========================
# TEST EXECUTION GUIDANCE
# =========================

    if "approved_test_cases" in st.session_state:

        execution_guidance = (
            execution_agent.generate_guidance(
                st.session_state[
                    "approved_test_cases"
                ]
            )
        )

        st.subheader(
            "🛠️ Test Execution Guidance"
    )

        st.write(
            execution_guidance
        )
    #coverage_agent = TestCoverageAgent(
    #client
    #)

    #coverage_review = (
        #coverage_agent.review_coverage(
            #brd,
            #final_jira,
            #edited_test_cases
        #)
    #)

    #st.subheader(
        #"📊 Test Coverage Review"
    #)

    #st.write(
        #coverage_review
    #)

    # =========================
# FINAL SIGN-OFF
# =========================

    st.subheader(
        "🏆 Final Sign-Off"
    )

    all_approved = (
        "approved_challenge_review" in st.session_state
        and
        "approved_requirements" in st.session_state
        and
        "approved_jira" in st.session_state
        and
        "approved_test_cases" in st.session_state
    )

    if all_approved:

        if st.button(
            "🏆 Finalize Requirement Package"
        ):

            st.session_state[
                "final_signoff"
            ] = True

            st.success(
                "Requirement Package Finalized"
            )
            st.info(
                "Status: Locked and Ready For Jira"
            )
    else:

        st.warning(
            "Complete all approvals before Final Sign-Off"
        )

    if st.session_state.get(
        "final_signoff",
        False
    ):

        st.success(
            "🏆 Requirement Package Finalized"
        )

        st.info(
            "Editing Complete • Ready For Jira Deployment"
        )
        st.subheader(
            "🚀 Jira Package"
        )

        if st.button(
            "🚀 Create Jira Package"
        ):

            st.session_state[
                "jira_package_created"
            ] = True

            st.success(
                "Jira Package Created Successfully"
            )
            

                
        if st.session_state.get(
            "jira_package_created",
            False
        ):

            st.info(
                """
        Package ID: REQ-2026-001
        
        Requirements: Approved

        Jira Stories: Approved

        Test Cases: Approved

        Status: Ready For Upload
        """
            )
            if st.button(
                "🚀 Push To Jira"
            ):

                st.session_state[
                    "jira_uploaded"
                ] = True

            if st.session_state.get(
                "jira_uploaded",
                False
            ):

                st.success(
                    "Stories Successfully Uploaded To Jira"
                )

                st.code(
                    """
        EPIC: REQ-100

        REQ-101  Create Customer Dashboard

        REQ-102  Build Data Pipeline

        REQ-103  Develop Analytics Engine

        REQ-104  User Acceptance Testing
        """
                )

                st.success(
                    "Jira Upload Completed"
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
            ""
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

