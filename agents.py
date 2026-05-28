
from openai import OpenAI


# =========================
# REQUIREMENT AGENT
# =========================

class RequirementAgent:

    def __init__(self, client):

        self.client = client


    def extract_requirements(self, text):

        prompt = f"""
Analyze the BRD below.

Extract:
- business objectives
- functional requirements
- operational requirements
- data requirements
- key modules

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
Generate enterprise High Level Design.

IMPORTANT:
This is a SQL-driven manufacturing intelligence platform.

The SQL database is the source of truth.

AI agents are used for:
- orchestration
- requirement understanding
- query generation
- insight generation
- executive summaries

The architecture must include:

1. SQL database layer
2. Data ingestion layer
3. AI orchestration layer
4. Query generation engine
5. Operational analytics layer
6. Pandas transformation layer
7. Streamlit visualization layer
8. Executive dashboard layer

Explain clearly:

- how SQL tables are joined
- join keys
- lineage flow
- operational workflow
- defect analytics
- bottleneck analytics
- customer impact analytics

Use these manufacturing tables:

1. PRODUCTION_DATA
   - MAT_ID
   - ORDER_NO
   - PROD_UNIT
   - ROUTE

2. DEFECT_DATA
   - MAT_ID
   - DEFECT_NAME
   - BLOCKING_DEFECT

3. ORDER_DATA
   - ORDER_NO
   - CUSTOMER_NAME
   - PROMISED_DELIVERY_DATE

4. MATERIAL_FLOW_DATA
   - MAT_ID_PREV
   - MAT_ID_NEXT

IMPORTANT JOIN LOGIC:

- PRODUCTION_DATA.MAT_ID
  joins with
  DEFECT_DATA.MAT_ID

- PRODUCTION_DATA.ORDER_NO
  joins with
  ORDER_DATA.ORDER_NO

- MATERIAL_FLOW_DATA.MAT_ID_NEXT
  joins with
  PRODUCTION_DATA.MAT_ID

Explain:
- why joins are needed
- operational purpose
- business impact
- SQL-driven architecture

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
Generate executive summary.

Include:
- business value
- operational impact
- AI benefits
- SQL analytics impact
- implementation recommendation

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

