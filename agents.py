
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
{PROFESSIONAL_STYLE}

You are a Senior Business Analyst.
Generate professional business requirements.

Output Style:
Professional and concise
Suitable for BA and Product Owner review
Avoid generic AI language
Avoid repetition
Focus only on actionable requirements

Structure:
Business Objective
Must Have Requirements
(Maximum 5 items)
Should Have Requirements
(Maximum 3 items)
Risks
Success Metrics

Rules:
Use bullet points
Keep output under one page
No unnecessary explanations
No assumptions unless explicitly stated

BRD:
{text}
"""

        response = self.client.chat.completions.create(

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

Data Source
- Where data comes from

Tables Used
- List tables if mentioned

Processing
- What calculations or transformations happen

Output
- Dashboard, report or KPI output

Users
- Who will use it

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
        solution
    ):

        prompt = f"""
{PROFESSIONAL_STYLE}

You are a Senior Delivery Manager.
Generate an executive summary.
Output Style:
Professional
Leadership focused
Concise
Decision-oriented
Structure:
Objective
Key Capabilities
(Maximum 5 bullets)
Business Impact
Key Risks
Expected Outcome
Rules:
Maximum 6 bullet points per section
Avoid repeating requirements
Avoid AI-generated language
No generic recommendations
Focus on business value and implementation readiness


Requirements:
{requirements}

HLD:
{hld}

Solution:
{solution}
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an executive AI consultant."
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

{PROFESSIONAL_STYLE}

You are a Solution Architect.

Generate a concise Mermaid architecture diagram.

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
                    "content": "Return only Mermaid diagram syntax."
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

- Return 5 to 8 process steps
- One step per line
- No bullets
- No numbering
- Keep each step short
- Use business language

Example:

Receive Data
Validate Data
Analyze Production
Identify Bottlenecks
Generate Insights
Review Results


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

Review the BRD and identify:

1. Missing Information
2. Questions To Clarify
3. Recommendations

Rules:

* Maximum 5 items per section
* Use bullet points
* Be specific to the business context
* Focus on missing business, data, operational and technical details
* Avoid generic AI language

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
                    "content": "You are an expert BA reviewer."
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

Requirement Completeness Score: XX%

Business Context: ✅ / ⚠️ / ❌
Functional Scope: ✅ / ⚠️ / ❌
Data Scope: ✅ / ⚠️ / ❌
Timeline: ✅ / ⚠️ / ❌
Success Metrics: ✅ / ⚠️ / ❌
Security Requirements: ✅ / ⚠️ / ❌

Implementation Readiness:
Ready / Needs Clarification / Not Ready

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
{PROFESSIONAL_STYLE}

You are a Senior Business Analyst.

Improve the BRD using the AI Challenge Review.

Rules:

- Keep concise
- Remove repetition
- Incorporate missing information where possible
- Improve clarity
- Improve implementation readiness
- Keep output professional

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
                    "content": "You are a senior enterprise business analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content


