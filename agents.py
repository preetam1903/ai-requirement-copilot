
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

        Include:
        - architecture
        - modules
        - integrations
        - AI components
        - data flow
        - dashboards

        Requirements:
        {requirements}
        """

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an enterprise solution architect."
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
        - AI architecture
        - deployment approach
        - implementation phases
        - operational workflow
        - agentic AI architecture

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
        You are a senior manufacturing data engineer.

        Generate executable Python Pandas code.

        STRICT RULES:

        - Generate ONLY executable Python code
        - No markdown
        - No explanations
        - Use Pandas
        - Use proper joins
        - Use safe null handling
        - Use route parsing logic
        - Generate NEXT_INSTALLATION dynamically

        Use these dataframe names:
        - production_df
        - defect_df
        - order_df
        - material_flow_df

        Include:
        - defect analysis
        - customer impact
        - bottleneck logic
        - next installation derivation
        - operational filtering

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
                    """
You are an enterprise manufacturing
AI analytics engineer.
"""
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
        - scalability
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

