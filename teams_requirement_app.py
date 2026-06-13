
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
    TestCaseAgent,
    BusinessScenarioAgent,
    AIUnderstandingAgent,
    DashboardPreviewAgent,
    ProjectManagerAgent,
    ChangeImpactAgent,
    ScreenAnalysisAgent,
    CurrentFutureStateAgent
)
from image_utils import (
    extract_red_region,
    image_to_bytes
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
# SCREEN UPLOAD
# =========================

uploaded_screens = st.file_uploader(
    "Upload Screens To Be Changed",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)



field_to_change = st.text_input(
    "Field To Be Changed",
    placeholder="Example: Postal Code"
)
change_reason = st.text_area(
    "Business Reason For Change",
    placeholder="Example: New country requires 6-character postal code",
    height=80
)

st.session_state["field_to_change"] = field_to_change
st.session_state["change_reason"] = change_reason

# =========================
# BRD GENERATOR
# =========================

#def generate_brd(requirement_text):
#
 #   prompt = f"""
#Convert the meeting information below
#into a professional Business Requirement Document.

#Include:




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

    screen_references = []

    if uploaded_screens:

        for screen in uploaded_screens:

            screen_references.append(
                screen.name
            )

    st.session_state[
        "screen_references"
    ] = screen_references
    
    meeting_agent = MeetingAgent(client)
    screen_agent = ScreenAnalysisAgent(
        client
    )

    state_agent = CurrentFutureStateAgent(
        client
    )
    screen_results = []

    if uploaded_screens:

        st.subheader(
            "📷 Uploaded Screens"
        )

        for screen in uploaded_screens:

            st.image(
                screen,
                caption=screen.name,
                width=600
            )

            image_bytes = screen.read()

            screen.seek(0)

            cropped_image = extract_red_region(
                image_bytes
            )

            cropped_bytes = image_to_bytes(
                cropped_image
            )

            st.image(
                cropped_image,
                caption="Detected Change Area",
                width=500
            )

            analysis = (
                screen_agent.analyze_screen(
                    cropped_bytes,
                    screen.name
                )
            )

            screen_results.append(
                {
                    "name": screen.name,
                    "analysis": analysis
                }
            )
            st.session_state[
                "screen_analysis"
            ] = screen_results

        if screen_results:

                combined_analysis = "\n\n".join(
                    [
                        item["analysis"]
                        for item in screen_results
                    ]
                )

                state_analysis = (
                    state_agent.generate_state_analysis(
                        combined_analysis,
                        change_reason
                    )
                )

                st.session_state[
                    "state_analysis"
                ] = state_analysis    
            
    st.subheader("DEBUG - Transcript Sent To AI")

    st.text_area(
        "Transcript",
        transcript_text,
        height=300
    )
    meeting_data = (
        meeting_agent.process_transcript(
            transcript_text
        )
    )
    scenario_agent = BusinessScenarioAgent(
        client
    )
    understanding_agent = AIUnderstandingAgent(
        client
    )
    dashboard_agent = DashboardPreviewAgent(
        client
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
    # business scenario preview
    understanding_input = (
        st.session_state.get(
            "approved_refined_brd",
            transcript_text
        )
    )

    ai_understanding = (
        understanding_agent.summarize_understanding(
            understanding_input
        )
    )

    st.subheader(
        "🧠 What AI Understood"
    )

    st.success(
        ai_understanding
    )
    
    scenario_input = (
        st.session_state.get(
            "approved_refined_brd",
            transcript_text
        )
    )

    scenario_preview = (
        scenario_agent.generate_scenarios(
            scenario_input
        )
    )
    dashboard_input = (
        st.session_state.get(
            "approved_refined_brd",
            transcript_text
        )
    )

    dashboard_preview = (
        dashboard_agent.generate_dashboard_preview(
            dashboard_input
        )
    )

    st.subheader(
        "🧪 Business Scenario Preview by AI"
    )

    scenarios = scenario_preview.split("Scenario")

    for scenario in scenarios:

        if not scenario.strip():
            continue

        if "Normal" in scenario:

            st.success(
                "🟢 Normal Scenario\n\n" +
                scenario
            )

        elif "Exception" in scenario:

            st.error(
                "🔴 Exception Scenario\n\n" +
                scenario
            )

        elif "Impact" in scenario:

            st.warning(
                "🟡 Business Impact Scenario\n\n" +
                scenario
            )

        else:

            st.info(
                scenario
            )   

    
    

# =========================
# EXPECTED DASHBOARD PREVIEW
# =========================

    st.subheader(
        "📊 Expected Dashboard Preview by AI"
    )

    st.success(
        dashboard_preview
    )



    # =========================
# MEETING ANALYSIS
# =========================

    st.subheader(
        "🧠 Meeting Analysis"
    )

    st.text_area(
        "Meeting Analysis",
        value=meeting_data,
        height=400
    )
    st.subheader(
        "🔄 Business Process Flow"
    )
    

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
    if uploaded_screens:

        st.subheader(
            "🔍 AI Screen Analysis"
        )

        for result in screen_results:

            with st.expander(
                result["name"]
            ):

                st.write(
                    result["analysis"]
                )
    if st.session_state.get(
        "state_analysis"
    ):

        st.subheader(
            "🎯 AI Change Analysis"
        )

        st.success(
            st.session_state[
                "state_analysis"
            ]
        )
# =========================
# BUILD FINAL BRD
# =========================

    brd = meeting_data

# -------------------------
# SCREEN REFERENCES
# -------------------------

    if st.session_state.get(
        "screen_references"
    ):

        brd += "\n\n"
        brd += "================================================\n\n"

        brd += "6A. SCREEN REFERENCES\n\n"

        for idx, screen_name in enumerate(
            st.session_state[
                "screen_references"
            ],
            start=1
        ):

            brd += (
                f"Screen {idx}\n"
            )

            brd += (
                f"File Name: {screen_name}\n"
            )

            brd += (
                "Purpose: Current screen to be modified.\n\n"
            )

# -------------------------
# FIELD IDENTIFICATION
# -------------------------

    if st.session_state.get(
        "field_to_change"
    ):

        brd += "\n"
        brd += "================================================\n\n"

        brd += "6B. FIELD IDENTIFICATION\n\n"

        brd += (
            f"Field Name: "
            f"{st.session_state['field_to_change']}\n\n"
        )

    # -------------------------
# SCREENSHOT SUMMARY
# -------------------------

    if st.session_state.get(
        "screen_analysis"
    ):

        brd += "\n"
        brd += "================================================\n\n"

        brd += (
            "6C. SCREENSHOT SUMMARY\n\n"
        )

        for idx, item in enumerate(
            st.session_state[
                "screen_analysis"
            ],
            start=1
        ):

            brd += (
            f"Screen {idx}\n\n"
            )

            brd += (
                f"File Name: "
                f"{item['name']}\n\n"
            )

            brd += (
                "AI Analysis Available "
                "In Screen Analysis Section\n\n"
            )

            brd += (
                "----------------------------------------\n\n"
            )
# -------------------------
# SCREEN ANALYSIS
# -------------------------

    if st.session_state.get(
        "screen_analysis"
    ):

        brd += "\n"
        brd += "================================================\n\n"

        brd += "6D. SCREEN ANALYSIS\n\n"

        for item in st.session_state[
            "screen_analysis"
        ]:

            brd += (
                f"Screenshot: "
                f"{item['name']}\n\n"
            )

            brd += (
                f"{item['analysis']}\n\n"
            )
    # -------------------------
# AI CHANGE ANALYSIS
# -------------------------

    if st.session_state.get(
        "state_analysis"
    ):

        brd += "\n"
        brd += "================================================\n\n"

        brd += "6E. AI CHANGE ANALYSIS\n\n"

        brd += (
            st.session_state[
                "state_analysis"
            ]
        )

        brd += "\n\n"
    # -------------------------
# FINANCE BA REVIEW
# -------------------------

    if st.session_state.get(
        "state_analysis"
    ):

        state_text = st.session_state[
            "state_analysis"
        ]

        review_text = ""

        if "ASSUMPTIONS" in state_text:

            assumptions_part = (
                state_text.split(
                    "ASSUMPTIONS"
                )[-1]
            )

            review_text += (
                "ASSUMPTIONS\n\n"
            )

            review_text += assumptions_part

        brd += "\n"
        brd += "================================================\n\n"

        brd += (
            "6F. FINANCE BA REVIEW\n\n"
        )

        brd += review_text

        brd += "\n\n"
# -------------------------
# BUSINESS JUSTIFICATION
# -------------------------

    if st.session_state.get(
        "change_reason"
    ):

        brd += (
            f"Business Reason: "
            f"{st.session_state['change_reason']}\n\n"
        )

# -------------------------
# CURRENT STATE
# -------------------------

    #if st.session_state.get(
    #    "field_to_change"
    #):

     #   brd += "CURRENT STATE\n\n"
#
 ##          f"Field '{st.session_state['field_to_change']}' "
    #        "is part of the current process.\n"
   #     )
#
 #       brd += (
  #          "Current functionality and behaviour "
   #         "to be confirmed by business.\n\n"
    #    )

# -------------------------
# FUTURE STATE
# -------------------------

    #if st.session_state.get(
     #   "field_to_change"
    #):

     #   brd += "FUTURE STATE\n\n"
#
 #       brd += (
  #          f"Field '{st.session_state['field_to_change']}' "
   #         "will be modified as per business requirements.\n"
    #    )
#
 #       brd += (
  #          "Updated validation, processing logic "
   #         "and business rules shall apply.\n\n"
    #    )

# -------------------------
# DISPLAY BRD
# -------------------------

    st.subheader(
        "📄 BRD Document View"
    )

    with st.expander(
        "Open BRD Document",
        expanded=True
    ):

        st.text(brd)
    st.subheader(
        "📄 Business Requirement Document"
    )

    st.text_area(
        "BRD",
        value=brd,
        height=700
    )

   
         # =========================
# REQUIREMENT COMPLETENESS
# =========================

    completeness_agent = RequirementCompletenessAgent(
        client
    )

    readiness_input = st.session_state.get(
        "approved_refined_brd",
        brd
    )

    completeness_review = (
        completeness_agent.assess_completeness(
            readiness_input
        )
    )
    import re

    score_match = re.search(
        r"(\d{1,3})\s*%",
        completeness_review
    )

    readiness_score = (
        score_match.group(1)
        if score_match
        else "0"
    )

    st.subheader(
        "📊 Requirement Readiness"
    )

    st.metric(
        "Readiness Score",
        f"{readiness_score}%"
    )

    with st.expander(
        "View Detailed Assessment"
    ):

        st.write(
            completeness_review
        )

        
    challenge_agent = AIChallengeAgent(
    client
    )

    challenge_review = (
    challenge_agent.challenge_requirements(
    brd
    )
    )

    st.subheader(
        "🔍 Business Clarifications"
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
# CHANGE IMPACT ANALYSIS
# =========================

    if "approved_refined_brd" in st.session_state:

        impact_agent = ChangeImpactAgent(
            client
        )

        impact_analysis = (
            impact_agent.analyze_impact(
                brd,
                st.session_state.get(
                    "approved_refined_brd"
                )
            )
        )

        st.subheader(
            "🔄 Requirement Change Impact Analysis"
        )

        with st.expander(
            "View Impact Assessment"
        ):

            st.write(
                impact_analysis
            )
    # =========================
    # REQUIREMENTS
    # =========================

    final_brd = st.session_state.get(
        "approved_refined_brd",
        brd
    )

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

    st.subheader("🏗️ Solution Summary")

    st.write(hld)
    diagram_agent = ArchitectureDiagramAgent(
    client
    )

    diagram = diagram_agent.generate_diagram(
        final_requirements,
        hld
    )

    st.subheader("🏛️ Solution Flow")

    st.markdown(diagram)
    


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
# AI PROJECT MANAGER
# =========================

    pm_agent = ProjectManagerAgent(
        client
    )

    project_plan = (
        pm_agent.generate_plan(
            final_requirements,
            final_jira
        )
    )

    st.subheader(
        "🤖 AI Project Manager"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Complexity",
        "Medium"
    )

    col2.metric(
        "Risk",
        "Medium"
    )

    col3.metric(
        "Estimated Effort",
        "6 weeks"
    )

    with st.expander(
        "View Delivery Plan"
    ):
        st.write(
            project_plan
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

        with st.expander(
            "View Execution Guide"
        ):

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

