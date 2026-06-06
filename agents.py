
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
{PROFESSIONAL_STYLE}

You are a Senior Solution Architect.
Generate a professional High Level Design.

Output Style:
Professional and concise
Suitable for architecture review
Avoid generic AI language
Avoid repetition
Structure:
Architecture Overview
Core Components
(Maximum 5)
Data Flow
Integrations
Security Considerations

Rules:
Use bullet points
Maximum 2 pages
Focus on implementation
No unnecessary explanations
Requirements:
{requirements}
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an enterprise manufacturing solution architect."
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
{PROFESSIONAL_STYLE}

Generate enterprise implementation solution.

Include:
- technology stack
- SQL architecture
- AI orchestration
- deployment architecture
- operational workflow
- dashboard layer
- analytics layer

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
                    "You are an enterprise AI architect."
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


{PROFESSIONAL_STYLE}

You are a Senior Business Analyst.

Analyze the transcript and identify the business process flow.

Rules:

* Maximum 10 steps
* One step per line
* Keep names short
* Return only process steps
* No explanations
* No numbering

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






