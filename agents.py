
from openai import OpenAI


PROFESSIONAL_STYLE = """
Output Style:

* Professional and concise
ƒ* Suitable for enterprise stakeholders
* Avoid generic AI language
* Avoid repetition
* Use bullet points where appropriate
* Focus on actionable information
* Avoid unnecessary explanations
* Write like a Senior Business Analyst or Architect
  """

GENERIC_BA_RULES = """
You are a Senior SAP Finance Business Analyst.

The solution must support any SAP Finance BAU change.

Examples include but are not limited to:

- Customer Master
- Vendor Master
- GL Master
- Cost Center
- Profit Center
- Tax Configuration
- Payment Terms
- Credit Management
- Workflow Approval
- Reporting
- Interfaces
- Master Data
- Configuration Changes

Use only information available from:

- Meeting Transcript
- Screen Analysis
- Configuration Findings

Do not optimise the output for any specific example.

Do not invent business users unless they can be reasonably inferred from SAP Module context.

Generate reusable business documentation suitable for any SAP Finance BAU requirement.

If information is missing:
- Raise Open Questions.
- Do not invent values.

If contradictions exist:
- Flag them.
- Do not resolve them automatically.
"""

# =========================
# REQUIREMENT AGENT
# =========================

class RequirementAgent:

    def __init__(self, client):

        self.client = client


    def extract_requirements(self, text):

        prompt = f"""
        You are a Business Analyst.

Create a simple list of business requirements.

Format:

REQ-001
<requirement>

REQ-002
<requirement>

REQ-003
<requirement>

Rules:

- Maximum 10 requirements
- One requirement per line
- Keep requirements short
- Business language only
- Avoid long descriptions
- Avoid architecture discussions
- Avoid implementation details
- Avoid AI terminology
- Avoid risks section
- Avoid success metrics section
- Avoid must-have / should-have grouping
- Mention SQL tables if available
- Mention Spotfire if applicable
- Focus only on what needs to be delivered

BRD:

{text}
"""
        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an experienced business analyst for SQL reporting and Spotfire dashboard solutions."
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
# HLD AGENT
# =========================

class HLDAgent:

    def __init__(self, client):

        self.client = client


    def generate_hld(self, requirements):

        prompt = f"""
        You are a Business Analyst.

Create a simple High Level Design.

Format:

📥 Data

⚙️ Analysis

📊 Dashboard

👥 Consumers

Rules:

- Maximum 3 bullets per section
- Business language only
- No architecture terminology
- No technical explanations
- No implementation details

Rules:

- Maximum 5 sections
- Maximum 1-2 bullets per section
- Keep it simple
- Business language only
- No architecture jargon
- No security discussion
- No cloud discussion
- No integrations unless explicitly mentioned
- Mention Spotfire if applicable

Requirements:

{requirements}
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an experienced business analyst who designs SQL and Spotfire reporting solutions."
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
# SOLUTION AGENT
# =========================

class SolutionAgent:

    def __init__(self, client):

        self.client = client


    def generate_solution(
        self,
        requirements,
        hld
    ):

        prompt = f"""
        Create a simple business solution overview.

Format:

Solution Flow
- How the solution works

Data Source
- SQL tables used

Processing
- Business calculations performed

Output
- Dashboard or report generated

Business Benefit
- Value delivered

Rules:

- Maximum 10 bullets
- Keep each bullet short
- Business language only
- Avoid AI terminology
- Avoid architecture terminology
- Avoid deployment discussions
- Avoid cloud discussions
- Mention Spotfire if applicable
- Focus on business outcome

Requirements:
{requirements}

HLD:
{hld}
"""
        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an experienced business analyst designing SQL and Spotfire reporting solutions."
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
# QUERY AGENT
# =========================

class QueryAgent:

    def __init__(self, client):

        self.client = client


    def generate_query(
        self,
        requirements,
        solution
    ):

        prompt = f"""
{PROFESSIONAL_STYLE}

Generate executable Python Pandas code.

STRICT RULES:

- Generate ONLY Python code
- No markdown
- No explanations
- Use Pandas
- Use proper joins
- Use safe null handling
- Generate NEXT_INSTALLATION dynamically

Use these dataframe names:
- production_df
- defect_df
- order_df
- material_flow_df

Requirements:
{requirements}

Solution:
{solution}
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are a manufacturing analytics engineer."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.1
        )

        return response.choices[0].message.content


# =========================
# INSIGHT AGENT
# =========================

class InsightAgent:

    def __init__(self, client):

        self.client = client


    def generate_summary(
        self,
        requirements,
        hld,
        solution=""
    ):

        prompt = f"""
You are a Business Leader.

Generate a concise Executive Summary.

Format:

Business Objective

* What problem is being solved

Key Deliverables

* Maximum 5 bullets

Business Benefits

* Maximum 5 bullets

Expected Outcome

* Maximum 3 bullets

Rules:

* Maximum 1 page
* Business language only
* Keep bullets short
* Avoid architecture terminology
* Avoid implementation terminology
* Avoid AI terminology
* Avoid technology stack discussions
* Avoid security discussions
* Focus on business value
* Mention Spotfire if applicable

Requirements:
{requirements}

Solution Summary:
{hld}
"""


        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are a manufacturing business leader focused on operational improvement."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )

        return response.choices[0].message.content

# =========================
# MEETING AGENT
# =========================

import json


class MeetingAgent:

    def __init__(self, client):
        self.client = client

    def process_transcript(self, transcript):

        prompt = f"""
You are a Senior SAP Finance Business Analyst.

{PROFESSIONAL_STYLE}

{GENERIC_BA_RULES}

Create a Business Requirement Document
If SAP MODULE information is provided:
If SAP MODULE information is provided:

Treat the SAP Module as primary business context.

If MODULE KNOWLEDGE is provided:

Use it to enrich the BRD.

Do not simply repeat transcript content.

Use module knowledge to infer:

- Typical business processes
- Common business users
- Scope of data
- Potential upstream impacts
- Potential downstream impacts
- Configuration impacts
- Testing impacts
- UAT scenarios

The generated BRD should combine:

1. Transcript Information
2. Screen Analysis Findings
3. Module Knowledge

Use module knowledge to improve:

- Explain The Business Process
- For Whom Is The Solution
- Scope Of Data
- Not In Scope
- Configuration Impact
- Testing Impact
- UAT Scenarios
- Open Questions

Do not invent facts.

Only infer logical business impacts and testing considerations that are normally associated with the selected SAP Module.

Use the SAP Module even if it is not explicitly discussed in the transcript.

IMPORTANT:

You MUST use ONLY the structure below.

Do NOT create any other sections.

Do NOT create:

* Executive Summary
* Business Objective
* Scope
* Functional Requirements
* Non Functional Requirements
* Data Requirements
* Risks
* Assumptions
* Expected Outcomes

Use ONLY information explicitly stated in the transcript.

Do NOT assume:
- SAP module
- T-Code
- Table names
- Screen names
- Field names
- Business users

If not explicitly mentioned, write:

To Be Confirmed

Do not invent SAP objects.
Business Validation Rules

Before generating requirements:

- Check for contradictions in the transcript.
- Check for inconsistent field lengths.
- Check for mismatches between field structure and total length.
- Check for conflicting business rules.

If inconsistencies are detected:

- Do not invent a solution.
- Highlight the inconsistency in Open Questions.
- Generate requirements using only confirmed information.

Do not leave sections blank.
Do not return "Inputs Missing" unless the transcript contains no useful information.
SCREEN ANALYSIS FINDINGS may be included in the transcript.

Treat SCREEN ANALYSIS FINDINGS as supporting evidence.

Use screen findings to enrich:

- Current State
- Future State
- Configuration Impact
- Testing Impact

When screen findings identify:

- field names
- current values
- validation rules
- configuration areas
- SAP modules
- navigation paths

these details MUST be referenced explicitly in:

D) Current State

E) Future State

G) Configuration Impact

Do not simply mention that a screen exists.
Use the extracted values.

If configuration values, validation rules, field names or navigation paths are identified from screenshots, incorporate them into the BRD where relevant.

Transcript remains the primary source.
If transcript specifies a field length, use ONLY the stated length.Never infer or calculate alternative lengths.

Do not ignore screen analysis findings.
Generate ONLY the following structure.

================================================

1. GENERAL INFORMATION

A) A) Explain The Business Process

Summarize the business process discussed in the transcript.

B) B) For Whom Is The Solution

Identify likely business users from the transcript.

C) Priority

If business impact involves:

- Billing
- Invoicing
- Customer communications
- Regulatory compliance
- Master data controls

Suggest:

High

and add:

"Business to confirm final priority."

Otherwise:

To Be Confirmed

================================================

2. PROBLEM / OPPORTUNITY

A) What The Current Process Is Doing

================================================

3. BUSINESS REQUIREMENTS

Generate requirements using this format only:

SR1
SR2
SR3
SR4
...

================================================

4. ADDITIONAL INFORMATION

A) New Functionality

================================================

5. SOLUTION REQUIREMENTS

A) Scope Of Data

B) Not In Scope

================================================

6. DETAILED BUSINESS PROCESS CHANGE

B) Screen Name

Only populate if explicitly mentioned in the transcript.
Otherwise write:
To Be Confirmed

C) Field Name

Example:
Examples:

Field Name
Validation Rule
Payment Term
Tax Code
Vendor Group
Customer Group
Approval Level
Cost Center
Profit Center

G) Process Change Summary

Where possible, present the change using a comparison table.

Example:

Example:

| Area | Current State | Future State |
|------|--------------|--------------|
| Process | Existing Process | Updated Process |
| Business Rule | Existing Rule | Updated Rule |
| Configuration | Existing Setup | Updated Setup |

Use areas that are relevant to the requirement.

Do not force specific rows.

If a table is not appropriate, use concise bullet points instead.

Use transcript findings and screen analysis findings where available.

================================================

H) Business Rule Changes

List new or modified business rules.

================================================

I) Configuration Impact

Where multiple configuration changes exist,
present them in table format.

Example:

Example:

| Area | Current Configuration | Required Change |
|------|----------------------|-----------------|
| Configuration Area | Existing Setup | Updated Setup |

Use actual configuration areas identified from screenshots where available.

If only one configuration change exists,
use concise bullets instead.

================================================

J) Testing Impact


F) Business Rule Changes

List new or modified business rules.

G) Configuration Impact

Identify SAP configuration or master data changes required.

Where screen analysis findings are available:

- Reference impacted configuration areas.
- Reference navigation paths if identified.

H) Testing Impact

Identify business processes requiring regression testing.

Where screen analysis findings are available:

- Include field validation testing.
- Include configuration testing.
- Include regression impacts.



================================================

7. UAT

Generate:

UAT-01
Scenario
Expected Result

UAT-02
Scenario
Expected Result

================================================


8. OPEN QUESTIONS

List unresolved business questions.

Include:

- Contradictions
- Missing values
- Missing country information
- Missing business decisions

If none exist write:

None
Return ONLY the sections above.
================================================
9. ASSUMPTIONS

List assumptions made based on available information.

Examples:

- Change applies only to the specified country.
- Existing customer records remain unchanged.
- Existing countries are unaffected.
- Customer Master remains the system of record.

If no assumptions exist, write:
None.
CONTRADICTION HANDLING

If requirements contain conflicting values:

- Do not choose one value.
- Do not create requirements using unconfirmed values.
- Move the inconsistency to Open Questions.
- Mark the requirement as:

"Business clarification required."

Example:

Example:

Requirement contains conflicting values.

Output:

Business clarification required.

Please confirm the correct business rule before implementation.

Output:

Business clarification required regarding final postal code format.

Example
D) PROCESS CHANGE SUMMARY

| Area | Current State | Future State |
|------|---------------|--------------|
| Process | Existing Process | Updated Process |
| Business Rule | Existing Rule | Updated Rule |

I) Configuration Impact

| Area | Current Configuration | Required Change |
|------|----------------------|-----------------|
| Configuration Area | Existing Setup | Updated Setup |

Business Rule Changes

<List business rules>

Configuration Impact

<List impacts>

Testing Impact

<List impacted processes>


Meeting Transcript:

{transcript}
"""
        print("========== TRANSCRIPT RECEIVED ==========")
        print(transcript)
        print("========================================")
        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior business analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        content = response.choices[0].message.content

        return content


# =========================
# JIRA AGENT
# =========================

class JiraAgent:

    def __init__(self, client):
        self.client = client

    def generate_jira(self, requirements):

        prompt = f"""
You are a Product Owner.

Generate a Jira Delivery Package.

Format:

EPIC
- Epic Name
- Business Goal

USER STORIES

For each story provide:

Story ID
Story Title
Business Value
Acceptance Criteria

Rules:

- Maximum 5 stories
- Maximum 2 acceptance criteria per story
- Business Value maximum 4 words
- Keep story titles short
- Avoid long descriptions
- Avoid paragraphs
- Make output presentation friendly
- Mention SQL tables if applicable

Requirements:

{requirements}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Jira expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content


# =========================
# TEST CASE AGENT
# =========================

class TestCaseAgent:

    def __init__(self, client):
        self.client = client

    def generate_test_cases(self, jira_output):

        prompt = f"""
You are a Business Tester.

Generate business validation scenarios.

For each test case provide:

Test Case ID

Validate

Check In

Expected Result

Rules:

- Maximum 8 test cases
- Maximum 4 lines per test case
- Use business language only
- Use short test names
- Mention table names when available
- Mention Spotfire pages when available
- Avoid long sentences
- Avoid QA terminology
- Avoid execution instructions
- Avoid detailed descriptions

Format:

TC-001 Test Name

Validate

Check In

Expected

Based On:

{jira_output}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a QA architect."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content
    
class ArchitectureDiagramAgent:

    def __init__(self, client):
        self.client = client

    def generate_diagram(self, requirements, hld):

        prompt = f"""

        You are a Business Analyst.

Create a simple Mermaid data flow diagram.

Show ONLY:

- SQL Database
- Source Tables or Data Sources
- Business Calculations
- Spotfire Dashboard
- Business Users

Rules:


- Use flowchart LR
- Create a left-to-right flow
- Maximum 5 boxes
- Combine all source tables into one SQL Database box
- Use only:
  SQL Database
  Business Calculations
  Spotfire Dashboard
  Business Users
- Avoid branching logic
- Avoid separate KPI boxes
- Avoid separate business rule boxes
- Keep the diagram executive-friendly

- Maximum 8 boxes
- Maximum 10 arrows
- Use simple business language
- Avoid architecture terminology
- Avoid security components
- Avoid monitoring components
- Avoid AI components
- Avoid cloud components
- Avoid deployment components
- Focus only on how data flows from source to dashboard
Do NOT create separate boxes for business rules.

Do NOT create separate boxes for calculations.

Combine all processing into a single box called:

Business Rules & KPI Calculations
Use this pattern only:

Source Data
      ↓
Business Rules & KPI Calculations
      ↓
Spotfire Dashboard
      ↓
Business Users
Create a maximum of:

- 3 source boxes
- 1 processing box
- 1 dashboard box
- 2 user boxes
Return ONLY Mermaid syntax.

Requirements:
{requirements}

HLD:
{hld}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You create simple business data flow diagrams using Mermaid syntax only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        temperature=0.1
        )

        return response.choices[0].message.content


# =========================

# BUSINESS PROCESS AGENT

# =========================

class BusinessProcessAgent:


    def __init__(self, client):
        self.client = client

    def generate_process_flow(self, transcript):

        prompt = f"""
You are a Business Process Consultant.

Generate a business process flow.

Rules:

- Return exactly 5 process steps
- Maximum 4 words per step
- One step per line
- No bullets
- No numbering
- Business language only
- Focus on business outcome
- Avoid technical terminology
- Avoid SQL references
- Avoid analytics jargon

Example:

Production Data
Blocked Coil Detection
Customer Impact Analysis
Spotfire Dashboard
Management Review


Transcript:

{transcript}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Return only business process steps."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        temperature=0.1
        )

        return response.choices[0].message.content

# =========================

# AI CHALLENGE AGENT

# =========================

class AIChallengeAgent:


    def __init__(self, client):
        self.client = client

    def challenge_requirements(self, brd):

        prompt = f"""

{PROFESSIONAL_STYLE}

{GENERIC_BA_RULES}

Act as a Senior SAP Finance Business Analyst.
Review the BRD for:

- Contradictory values
- Inconsistent lengths
- Missing countries
- Missing business owners
- Missing priorities
- Missing scope boundaries
- Missing data migration requirements
- Missing interface impacts

Raise these as OPEN QUESTIONS.
Review the BRD and produce ONLY the following sections.

================================================

OPEN QUESTIONS

================================================

List business questions that must be answered before implementation.

================================================

ASSUMPTIONS

================================================

List assumptions currently being made.

================================================

DEPENDENCIES

================================================

List systems, teams, approvals, interfaces or data dependencies.

================================================

RISKS

================================================

List implementation or business risks.

================================================

BUSINESS DECISIONS REQUIRED

================================================

List decisions that business stakeholders must make.


Rules:

- Finance BAU focus
- Do not rewrite BRD
- Be concise
- Maximum 5 items per section

Do NOT discuss:
- Security frameworks
- Cloud architecture
- Governance frameworks
- Monitoring frameworks
- Microservices
- Deployment architecture
- AI architecture

Only identify information required before development can begin.

Examples:

* Timeline not specified
* Active vs historical data not specified
* Product category not specified
* User volume not specified
* Success criteria not defined
Example:

If a requirement contains contradictory information:

Raise:

OPEN QUESTION

The requirement contains conflicting business rules.

Please confirm the expected behaviour.

Raise:

OPEN QUESTION

The requirement contains conflicting business rules.

Please confirm the expected behaviour.

BRD:

{brd}
"""


        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced business analyst reviewing SQL and Spotfire reporting requirements."
                },
                {
                "role": "user",
                "content": prompt
                }
            ],
        temperature=0.1
        )

        return response.choices[0].message.content

# =========================

# TEST COVERAGE AGENT

# =========================

class TestCoverageAgent:


    def __init__(self, client):
        self.client = client

    def review_coverage(
        self,
        brd,
        jira_output,
        test_cases
    ):

        prompt = f"""


{PROFESSIONAL_STYLE}

You are a Senior QA Architect.

Review the BRD, Jira Stories and Test Cases.

Generate:

1. Covered Areas
2. Potential Missing Tests
3. Coverage Assessment

Rules:

* Maximum 5 bullets per section
* Keep output concise
* Focus on gaps
* Identify missing negative tests
* Identify missing edge cases
* Identify missing security or performance tests

BRD:
{brd}

Jira Stories:
{jira_output}

Test Cases:
{test_cases}
"""


        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior QA architect."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        temperature=0.1
        )

        return response.choices[0].message.content

# =========================
# REQUIREMENT COMPLETENESS AGENT
# =========================

class RequirementCompletenessAgent:

    def __init__(self, client):
        self.client = client

    def assess_completeness(self, brd):

        prompt = f"""
{PROFESSIONAL_STYLE}

You are a Senior Delivery Architect.

Review the BRD.

Return in this format:

Requirement Readiness Score: XX%

Business Objective: ✅ / ⚠️ / ❌
Data Sources Identified: ✅ / ⚠️ / ❌
Tables Identified: ✅ / ⚠️ / ❌
KPIs Defined: ✅ / ⚠️ / ❌
Dashboard Requirements: ✅ / ⚠️ / ❌
Business Users Identified: ✅ / ⚠️ / ❌

Overall Status:
Ready / Needs Clarification / Not Ready

Missing Information:
- Maximum 5 bullets

Rules:

- Keep output concise
- Business language only
- Focus on reporting and analytics requirements
- Mention SQL tables if available
- Mention Spotfire if applicable
- Do not discuss security frameworks
- Do not discuss cloud architecture
- Do not discuss deployment architecture
- Do not discuss governance frameworks
BRD:

{brd}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an enterprise delivery reviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content

# =========================
# REQUIREMENT REFINEMENT AGENT
# =========================

class RequirementRefinementAgent:

    def __init__(self, client):
        self.client = client

    def refine_requirements(
        self,
        brd,
        challenge_review
    ):

        prompt = prompt = f"""
You are a Senior SAP Finance Business Analyst.

Refine the BRD using the challenge review.

Maintain EXACTLY the same BRD structure.

Do NOT create new sections.

Do NOT create:

- Executive Summary
- Business Objective
- Required Data
- Expected Output
- Business Benefits
- Open Questions

Update only missing information.

Return ONLY:

1. GENERAL INFORMATION

A) Explain The Business Process

B) For Whom Is The Solution

C) Priority

================================================

2. PROBLEM / OPPORTUNITY

A) What The Current Process Is Doing

================================================

3. BUSINESS REQUIREMENTS

SR1
SR2
SR3

================================================

4. ADDITIONAL INFORMATION

A) New Functionality

================================================

5. SOLUTION REQUIREMENTS

A) Scope Of Data

B) Not In Scope

================================================

6. DETAILED BUSINESS PROCESS CHANGE

A) T-Code

B) Screen Where Change Needs To Take Place

C) Business Rule Changes

================================================

7. UAT

UAT-01
Scenario
Expected Result

UAT-02
Scenario
Expected Result

Original BRD:

{brd}

Challenge Review:

{challenge_review}
"""
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced business analyst for SQL reporting and Spotfire dashboard projects."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content

# =========================
# TEST EXECUTION GUIDANCE AGENT
# =========================

class TestExecutionGuidanceAgent:

    def __init__(self, client):
        self.client = client

    def generate_guidance(self, test_cases):

        prompt = f"""
You are a QA Lead.

Generate concise Test Execution Guidance.

For each approved test case provide:

Execution Method

Where To Validate

Pass Criteria

Business Owner

Rules:

* Maximum 3 lines per test case
* Keep it concise
* Business language only
* Mention table names when available
* Mention Spotfire pages when available
* Avoid technical testing terminology
* Avoid detailed step-by-step instructions
* Avoid SQL query instructions
* Avoid implementation details
* Focus on business validation

Example:

TC-001 Next Production Unit

Validate:
Next unit calculation

Check In:
Production Status Table
Spotfire Dashboard

Expected Result:
Next unit matches production route

Test Cases:

{test_cases}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an business focused QA lead for manufacturing SQL and Spotfire solutions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content

# =========================
# BUSINESS SCENARIO AGENT
# =========================

class BusinessScenarioAgent:

    def __init__(self, client):
        self.client = client

    def generate_scenarios(self, requirements):

        prompt = f"""
You are a manufacturing business analyst.

Generate 3 sample business scenarios.

Format:

Scenario 1 - Normal Case

Scenario 2 - Exception Case

Scenario 3 - Business Impact Case

For each scenario provide:

Coil ID
Current Stage
Issue/Defect
Expected Outcome
Dashboard Behaviour

Rules:

- Use realistic sample values
- Keep concise
- Business language only
- Maximum 5 lines per scenario
- Focus on expected business outcome
- Mention Spotfire if applicable

Requirements:

{requirements}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You create realistic manufacturing business scenarios."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

# =========================
# AI UNDERSTANDING AGENT
# =========================

class AIUnderstandingAgent:

    def __init__(self, client):
        self.client = client

    def summarize_understanding(
        self,
        transcript
    ):

        prompt = f"""
You are a Business Analyst.

Review the meeting transcript.

Identify the top 5 things the AI believes the business wants.

Format:

✅ Item 1

✅ Item 2

✅ Item 3

✅ Item 4

✅ Item 5

Rules:

- Maximum 5 items
- Maximum 5 words per item
- Business language only
- No technical jargon
- No explanations
- Focus on business outcomes

Transcript:

{transcript}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role":"system",
                    "content":
                    "You summarize business understanding."
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content
# =========================
# DASHBOARD PREVIEW AGENT
# =========================

class DashboardPreviewAgent:

    def __init__(self, client):
        self.client = client

    def generate_dashboard_preview(
        self,
        requirement
    ):

        prompt = f"""
You are a Business Intelligence Architect.

Review the requirement.

Generate the top dashboard KPIs.

Format:

📊 KPI 1

📊 KPI 2

📊 KPI 3

📊 KPI 4

📊 KPI 5

Rules:

- Maximum 5 KPIs
- KPI names only
- Business language only
- No explanations
- Avoid technical terminology
- Focus on business value

Requirement:

{requirement}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You design executive dashboards."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content

# =========================
# PROJECT MANAGER AGENT
# =========================

class ProjectManagerAgent:

    def __init__(self, client):
        self.client = client

    def generate_plan(
        self,
        requirements,
        jira_output
    ):

        prompt = f"""
You are a Senior IT Project Manager.

Review the requirements and Jira stories.

Generate:

Project Complexity

Risk Level

Estimated Effort

Requirements Review
Solution Design
Development
Testing
UAT

Recommended Team

Dependencies

Rules:

- Keep concise
- Use business language
- Maximum one page
- Focus on planning
- Avoid technical implementation details

Requirements:

{requirements}

Jira Stories:

{jira_output}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an enterprise project manager."
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
# CHANGE IMPACT AGENT
# =========================

class ChangeImpactAgent:

    def __init__(self, client):
        self.client = client

    def analyze_impact(
        self,
        original_brd,
        refined_brd
    ):

        prompt = f"""
You are a Senior Delivery Architect.

Compare:

Original BRD

and

Refined BRD

Generate:

New Information Added

Impacted Areas

Requirements Impact

Jira Impact

Test Case Impact

Impact Level
(Low / Medium / High)

Recommended Action

Rules:

- Keep concise
- Use business language
- Maximum one page
- Focus on delivery impact

Original BRD:

{original_brd}

Refined BRD:

{refined_brd}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an enterprise delivery architect."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content

import base64

class ScreenAnalysisAgent:

    def __init__(self, client):
        self.client = client

    def analyze_screen(
        self,
        image_bytes,
        image_name,
        analysis_mode
    ):

        base64_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        response = self.client.chat.completions.create(

            model="gpt-4.1",

            messages=[

                {
                    "role": "user",
                    "content": [

                        {
                            "type": "text",
                            "text": f"""
        

Analysis Mode:
{analysis_mode}

Screenshot Name:
{image_name}
================================================

You are a Senior SAP Finance Business Analyst.

The analysis must support ANY SAP Finance BAU change.

Examples include:

- Customer Master
- Vendor Master
- Payment Terms
- Tax Configuration
- Workflow Approval
- Cost Center
- Profit Center
- GL Master
- Reporting
- Interfaces

Do NOT assume:

- Postal Code
- Customer Master
- Address Validation

unless explicitly visible in the screenshot.

Extract ONLY what is visible.

Do not invent SAP objects.

Do not infer values not shown on screen.

================================================


IF Analysis Mode = Field Change

Focus ONLY on the highlighted field.

Ignore unrelated areas.


Return ONLY in this format.

FIELD_NAME: <Field Name>

CURRENT_VALUE: <Current Value>

CURRENT_CONFIGURATION: <Configuration or Validation>

BUSINESS_PURPOSE: <Business Purpose>

POTENTIAL_IMPACT: <Likely Change Impact>

If a field label and a field property are both visible:

Use the BUSINESS FIELD name.

Examples:

Correct:
FIELD_NAME: Postal Code

Incorrect:
FIELD_NAME: Length

Correct:
FIELD_NAME: Payment Terms

Incorrect:
FIELD_NAME: Days

Correct:
FIELD_NAME: Tax Code

Incorrect:
FIELD_NAME: Value
================================================

IF Analysis Mode = Navigation / Process Flow

Focus on the complete screen.

Return:

SCREEN_NAME: <Screen Name>

NAVIGATION_PATH: <Navigation Path>

SAP_MODULE: <SAP Module>

CONFIGURATION_AREA: <Configuration Area>

BUSINESS_PURPOSE: <Business Purpose>

Return values on the SAME line as labels.

Do not return markdown.

Do not return explanations.

Return ONLY the structure.

================================================

Keep output concise.

Do not explain AI reasoning.

Return professional SAP BA language only.

"""
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                "url":
                                f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],

            temperature=0.1
        )

        return response.choices[0].message.content

class CurrentFutureStateAgent:

    def __init__(self, client):
        self.client = client

    def generate_state_analysis(
        self,
        screen_analysis,
        business_reason
    ):

        prompt = f"""
You are a Senior SAP Finance Business Analyst.
{GENERIC_BA_RULES}

Generate a professional Finance BAU Change Analysis.

Use EXACTLY the structure below.

================================================
CHANGE SUMMARY
==============

Generate a table using the format:

| Area | Current State | Future State |
| ---- | ------------- | ------------ |
| ...  | ...           | ...          |

Include 3-5 rows where possible.

Areas may include:

* Process
* Business Rule
* Configuration
* Data Element
* Validation
* Approval Logic
* Reporting
* Controls

================================================
CONFIGURATION IMPACT
====================

* Identify SAP objects/configuration likely impacted.

================================================
TESTING IMPACT
==============

* Identify business scenarios requiring testing.

================================================
ASSUMPTIONS
===========

* Maximum 5 bullets.

================================================
OPEN QUESTIONS
==============

* Maximum 5 questions.


CURRENT STATE
=============

* Describe how the process works today.
* Mention current SAP behaviour.
* Mention current limitations, manual activities or controls.

================================================
FUTURE STATE
============

* Describe the expected behaviour after implementation.
* Explain the business benefit.
* Explain process, validation or control improvements.

================================================
CONFIGURATION IMPACT
====================

* Identify likely SAP configuration areas impacted.
* Mention business rules, validations, master data or process controls.
* Be practical and SAP Finance focused.

================================================
TESTING IMPACT
==============

* Identify business scenarios requiring testing.
* Include positive, negative and regression testing.
* Focus on Finance BAU scenarios.

================================================

ASSUMPTIONS
===========

* Identify assumptions made due to missing information.
* Keep assumptions business focused.
* Maximum 5 bullets.

================================================
OPEN QUESTIONS
==============

* Generate questions a Senior Finance BA would ask.
* Focus on:

  * Scope
  * Reporting
  * Interfaces
  * Controls
  * Security
  * Data Migration
  * Testing
* Maximum 5 questions.

Rules:

* Use professional BRD language.
* Be specific.
* Avoid generic statements.
* Do not write "To Be Confirmed".
* Do not repeat screenshot text.
* Focus on Finance business requirements.
* Output must be suitable for inclusion in a BRD.

Screen Analysis:
{screen_analysis}

Business Requirement:
{business_reason}



Return structured output.
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content
