
from openai import OpenAI

PROFESSIONAL_STYLE = """
Output Style:

* Professional and concise
* Suitable for enterprise stakeholders
* Avoid generic AI language
* Avoid repetition
* Use bullet points where appropriate
* Focus on actionable information
* Avoid unnecessary explanations
* Write like a Senior Business Analyst or Architect
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
{PROFESSIONAL_STYLE}

You are a Senior Business Analyst.

Analyze the meeting transcript.

Extract:

- Project Name
- Business Objective
- Stakeholders
- Functional Requirements
- Non Functional Requirements
- Risks
- Assumptions
- Action Items
- Open Questions
- Success Metrics

Return ONLY valid JSON.

Transcript:

{transcript}
"""

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

        try:
            return json.loads(content)

        except:
            return {
                "business_objective": content
            }


# =========================
# JIRA AGENT
# =========================

class JiraAgent:

    def __init__(self, client):
        self.client = client

    def generate_jira(self, requirements):

        prompt = f"""
{PROFESSIONAL_STYLE}

Generate:

1. Epic
2. Features
3. User Stories
4. Acceptance Criteria
5. Story Points
6. Priority

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
{PROFESSIONAL_STYLE}

Generate:

- Functional Test Cases
- Negative Test Cases
- UAT Test Cases
- Expected Results

Based on:

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

You are a Senior Business Analyst and Solution Architect.

Review the BRD and identify business gaps.

Output Format:

Missing Information
- Missing business details

Questions To Clarify
- Questions for business users

Readiness Status
- Ready
- Needs Clarification
- Not Ready

Rules:

- Maximum 5 bullets per section
- Keep each bullet short
- Business language only
- Focus on missing business information
- Focus on missing data requirements
- Focus on missing reporting requirements
- Focus on missing dashboard requirements
- Mention SQL tables if relevant
- Mention Spotfire if relevant

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

        prompt = f"""
        You are a Business Analyst.

Refine the BRD using the Challenge Review.

Output Format:

1. Business Objective
- What problem is being solved

2. Required Data
- Tables, reports or data needed

3. Expected Output
- Dashboard, report or KPI output

4. Business Benefits
- Expected value

5. Open Questions
- Missing information requiring clarification

Rules:

- Maximum 15 bullets total
- Keep each bullet short
- Business language only
- Remove repetition
- Avoid architecture terminology
- Avoid AI terminology
- Avoid implementation details
- Avoid security discussions unless mentioned
- Avoid enterprise consulting language
- Mention SQL tables if available
- Mention Spotfire if applicable

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

For each test case provide:

Test Case
Validate
Check In
Expected Result

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
