import streamlit as st

def render_xray(trace_store):

    traces = trace_store.get_traces()

    for trace in traces:

        with st.expander(
            f"🔍 {trace.name}"
        ):
            st.subheader(
                "👤 WHO - Agent Execution"
            )
            st.write("### Agent")

            st.success(trace.name)
            st.write("### Mission")
            st.write("### Responsibility")

            st.success("""
            ✓ Read transcript

            ✓ Understand business discussion

            ✓ Generate BRD

            ✓ Pass output to next step
            """)
            st.info(
                trace.purpose
            )

            st.write("### Why was I Invoked")
            st.info(trace.why_called)
            st.write("### Agent Decision")

            st.info(f"""
            The system detected a transcript upload.

            {trace.name} was automatically selected because it specializes in converting business discussions into structured BRD documents.
            """)
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Input Tokens",
                    trace.input_tokens
                )

            with col2:
                st.metric(
                    "Output Tokens",
                    trace.output_tokens
                )

            with col3:
                st.metric(
                    "Cost",
                    f"₹{trace.estimated_cost}"
                )

            st.write("### 📥 Inputs Received")
            st.text_area(
                "Input",
                trace.input_data,
                height=200
            )
            st.success("""
            ✓ Meeting Transcript
    
            ✓ Business Context

            ✓ Knowledge Base

            ✓ Screen Analysis
            """)

            with st.expander(
                "📜 View Prompt Used"
            ):

                st.text_area(
                    "Prompt",
                    trace.prompt,
                    height=300
                )

            with st.expander(
                "📤 View Generated Output"
            ):

                st.text_area(
                    "Output",
                    trace.output_data,
                    height=250
                )


            

        
            with st.expander(
                "📨 WHAT - Prompt Construction"
            ):

                

                

            

               

                st.write("### Prompt Size")

                st.metric(
                    "Characters",
                    len(trace.prompt)
                )
                raw_size = len(trace.input_data)

                final_size = len(trace.prompt)

                growth = round(
                    ((final_size - raw_size) / max(raw_size,1)) * 100,
                    1
                )
                st.write("### Prompt Health")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Prompt Size",
                        f"{len(trace.prompt):,} chars"
                    )

                with col2:
                    st.metric(
                        "Expansion",
                        f"{growth}%"
                    )
                
                

                st.info(
                    "The LLM converts the input into tokens, combines it with instructions and predicts the next words to generate the response."
                )
                st.write("### Prompt Construction X-Ray")

                st.code("""
                Business Transcript
                        +
                Knowledge Base
                        +
                Screen Analysis
                        +
                Agent Instructions

                        ↓

                Final Prompt

                        ↓

                Send To LLM
                """)
                


# Then Add Dynamic Prompt Preview


                st.success("""
                Prompt Engineering controls:

                • What AI knows

                • What AI ignores

                • Output structure

                • Output quality

                The model is the engine.
                The prompt is the steering wheel.
                """)


                st.write("### 🔄 Prompt Evolution X-Ray")

                st.write("### Stage 1 - Raw Business Input")

                st.text_area(
                    "Original Transcript",
                    trace.input_data[:500],
                    height=120
                )

                st.write("### Stage 2 - Knowledge Added")

                st.code("""
                Customer Master Data

                Invoice Processing

                Country Validation

                Customer Communication
                """)

                st.write("### Stage 3 - Agent Instructions Added")

                st.code("""
                You are a Senior Business Analyst.

                Generate a BRD.

                Identify business requirements.

                Identify risks.

                Generate structured output.
                """)

                st.write("### Stage 4 - Final Prompt")

                st.success(
                    f"Prompt Size = {len(trace.prompt)} Characters"
                )
                st.write("### 🔍 Prompt Difference X-Ray")

                raw_size = len(trace.input_data)

                final_size = len(trace.prompt)

                added_size = final_size - raw_size

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "User Input",
                        f"{raw_size:,}"
                    )

                with col2:
                    st.metric(
                        "AI Added",
                        f"{added_size:,}"
                    )

                with col3:
                    st.metric(
                        "Final Prompt",
                        f"{final_size:,}"
                    )

                st.write("### Prompt Growth Analysis")

                

                st.metric(
                    "Prompt Expansion",
                    f"{growth}%"
                )
                st.write("### What AI Added")

                added_items = []

                prompt_text = trace.prompt.lower()

                if "customer" in prompt_text:
                    added_items.append("✓ Customer Master Knowledge")

                if "invoice" in prompt_text:
                    added_items.append("✓ Invoice Processing Context")

                if "postal" in prompt_text:
                    added_items.append("✓ Postal Code Validation Rules")

                if "country" in prompt_text:
                    added_items.append("✓ Country-Specific Business Rules")

                if not added_items:
                    added_items = [
                        "✓ Business Domain Knowledge",
                        "✓ Requirement Engineering Guidance",
                        "✓ Structured Output Instructions"
                    ]

                st.success("\n\n".join(added_items))
                st.write("### Why The Prompt Grew")

                st.info("""
                The AI system enriches the original transcript with:

                ✓ Business Context

                ✓ Domain Knowledge

                ✓ Agent Instructions

                ✓ Output Structure

                This additional information helps improve response quality and consistency.
                """)
                st.write("### Final Prompt Preview")

                st.text_area(
                    "Prompt Preview",
                    trace.prompt[:2500],
                    height=300
                )
                st.write("### 🧠 How GPT Predicts The Next Word")

                clean_text = (
                    trace.output_data
                    .replace("=", " ")
                    .replace("\n", " ")
                )

                words = clean_text.split()

                if len(words) > 30:

                    start_position = min(
                        20,
                        len(words) - 5
                    )

                    current_text = " ".join(
                        words[start_position:start_position+3]
                    )

                    predicted_word = words[
                        start_position+3
                    ]

                    st.write("### Current Context")

                    st.code(current_text)

                    st.write(
                        "### Possible Next Token Predictions"
                    )

                    st.code(
                        f"""
                {predicted_word}      82%
                alternative_1   10%
                alternative_2    5%
                alternative_3    3%
                """
                    )

                    st.write("### Selected Token")

                    st.success(predicted_word)

                    st.write(
                        "### Generated Sequence"
                    )

                    st.info(
                        f"{current_text} {predicted_word}"
                    )
                    
                else:

                    st.warning(
                        "Not enough output available."
                    )

            with st.expander(
                "🧠 Neural Network X-Ray"
            ):

                st.code("""
                Business Transcript
                    ↓
                Tokenization
                    ↓
                Embeddings
                    ↓
                Meaning Extraction
                    ↓
                Concept Discovery
                    ↓
                Relationship Discovery
                    ↓
                Risk Analysis
                    ↓
                Requirement Generation
                """)

                st.info("""
            The LLM does not understand words directly.

            Each word is converted into numbers called embeddings.

            These embeddings are processed through multiple neural network layers to identify patterns and relationships.
            """)

                sample_words = trace.input_data.split()[:5]

                st.write("### Embedding Example")

                st.code("""
                Business Word

                Postal Code

                    ↓

                Embedding Vector

                [0.24, -0.91, 0.67, 0.11, ...]

                    ↓

                Meaning Understood By AI

                Address Validation
                """)

                st.info("""
                The neural network cannot understand words directly.

                It converts words into embeddings (numbers).

                Embeddings help the model identify meaning and relationships between concepts.
                """)
                st.write("### Related Concepts Discovered")

                st.code("""
                Postal Code
                      ↓
                Customer Address
                      ↓
                Invoice Address
                      ↓
                Customer Communication
                """)

                st.write("### AI Reasoning Layers")

                st.code("""
                Layer 1

                Important Terms Detected

                ✓ Postal Code

                ✓ Customer

                ✓ Invoice

                ✓ Country

                    ↓

                Layer 2

                Business Concepts Detected

                ✓ Address Validation

                ✓ Customer Master

                ✓ Invoice Processing

                        ↓

                Layer 3

                Relationships Identified

                Postal Code
                      ↓
                Customer Address
                      ↓
                Invoice Delivery

                    ↓

                Layer 4

                Business Risk Identified

                Incorrect Postal Code
                      ↓
                Invoice Delivery Failure

                    ↓

                Layer 5

                Requirement Generated

                Enable support for
                11-character postal code
                """)
                st.write("### Final AI Decision")

                st.success("""
                Business Problem

                Incorrect postal code may cause invoice delivery failure

                ↓

                Recommended Requirement

                Enable support for 11-character postal code validation
                """)

                st.write("### AI Focus Areas")

                st.code("""
                Postal Code          ██████████

                Invoice Address      ████████

                Customer Master      ███████

                Country Validation   █████

                Communication Risk   ███
                """)

                st.info("""
                The attention mechanism helps the model focus on the concepts that are most important to solving the business problem.
                """)

            with st.expander(
                "🏭 How-Production X-Ray"
            ):
                st.write("### Business Requirement Journey")

                st.code("""
                👤 Business User
                    ↓

                📄 Transcript Upload
                    ↓

                🤖 Agent Selection
                    ↓

                📨 Prompt Construction
                    ↓

                🧠 Azure OpenAI
                    ↓

                📋 BRD Generation
                    ↓

                🛡 Governance Check
                    ↓

                👤 Human Approval
                    ↓

                📁 Final BRD
                """)

                st.info("""
                This shows how a business requirement moves through the AI platform from transcript upload to final approved BRD.
                """)
                st.write("### 🏗 Production Components Explained")

                st.code("""
                🌐 Streamlit

                What It Does
                Provides the user interface.

                Why Needed
                Allows business users to interact with AI.

                ────────────────────────────

                ⚙️ FastAPI

                What It Does
                Provides APIs between UI and AI services.

                Why Needed
                Separates frontend from backend.

                ────────────────────────────

                🤖 Agent Orchestrator

                What It Does
                Coordinates multiple AI agents.

                Why Needed
                Controls execution sequence and data flow.

                ────────────────────────────

                📨 Prompt Service

                What It Does
                Builds the final prompt sent to the LLM.

                Why Needed
                Combines transcript, knowledge and instructions.

                ────────────────────────────

                🧠 Azure OpenAI

                What It Does
                Performs reasoning and generation.

                Why Needed
                Creates BRDs, requirements and recommendations.

                ────────────────────────────

                🗄 SQL Database

                What It Does
                Stores transcripts, outputs and audit history.

                Why Needed
                Provides persistence and traceability.

                ────────────────────────────

                📦 Docker

                What It Does
                Packages the application into a portable container.

                Why Needed
                Ensures the application runs consistently everywhere.

                ────────────────────────────

                ☁ Azure Container Apps

                What It Does
                Runs Docker containers in production.

                Why Needed
                Provides scalability and enterprise hosting.
                """)

                st.write("### 🎼 Agent Orchestration Flow")

                st.code("""
                📄 Transcript
                    ↓

                🎼 Agent Orchestrator
                    ↓

                🤖 Meeting Agent
                    ↓

                🧠 AI Understanding Agent
                    ↓

                ⚠ Challenge Agent
                    ↓

                🏗 HLD Agent
                    ↓

                🧪 Test Case Agent
                    ↓

                📋 Final Delivery Package
                """)

                st.info("""
                The Agent Orchestrator acts like a project manager.

                It decides which agent runs next, passes outputs between agents and ensures the workflow completes successfully.
                """)

                st.write("### 🚀 Production Roadmap")

                st.code("""
                Phase 1

                Demo Platform

                Duration
                1 Week

                Components

                ✓ Streamlit

                ✓ OpenAI

                ✓ Core Agents

                ✓ X-Ray Framework


                    ↓


                Phase 2

                Pilot Deployment

                Duration
                2-3 Weeks

                Components

                ✓ FastAPI

                ✓ SQL Database

                ✓ Monitoring

                ✓ Authentication

                ✓ Audit Logs


                    ↓


                Phase 3

                Enterprise Production

                Duration
                4-6 Weeks

                Components

                ✓ Docker

                ✓ Azure Container Apps

                ✓ CI/CD Pipeline

                ✓ Governance Controls

                ✓ Human Approval Workflow

                ✓ Enterprise Monitoring
                """)

                st.success("""
                Estimated Journey

                Demo → Pilot → Production

                Approximately 6-10 Weeks depending on enterprise requirements.
                """)

                st.write("### 🛡 Failure Handling")

                st.code("""
                Azure OpenAI Failure
                    ↓

                Retry Request
                    ↓

                Fallback Model
                    ↓

                Log Error
                    ↓

                Notify Support Team
                    ↓

                User Notification
                """)

                st.info("""
                Production systems must handle failures gracefully.

                The platform should automatically retry requests, log issues and notify support teams before users are impacted.
                """)

                st.write("### 📊 Production Monitoring")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Success Rate",
                        "99.2%"
                    )

                with col2:
                    st.metric(
                        "Avg Response",
                        "2.4 sec"
                    )

                with col3:
                    st.metric(
                        "Availability",
                        "99.9%"
                    )

                st.success("""
                Monitoring Tracks

                ✓ Response Time

                ✓ Token Usage

                ✓ Cost

                ✓ Errors

                ✓ Agent Failures

                ✓ System Health
                """)



                
                st.write("### How This Demo Works Today")

                st.code("""
            Business User
                ↓
            Streamlit UI
                ↓
            Meeting Agent
                ↓
            Prompt
                ↓
            OpenAI API
                ↓
            Generated BRD
                ↓
            Business User
            """)

                st.write("### How Production Deployment Works")

                st.code("""
            Business User
                ↓
            Web Application
                ↓
            FastAPI Service
                ↓
            Agent Orchestrator
                ↓
            Prompt Service
                ↓
            Azure OpenAI
                ↓
            Response
                ↓
            Database
                ↓
            Audit Logs
            """)

                st.info("""
            Production systems separate UI, AI services,
            data storage and monitoring into independent components.
            """)
                st.write("### Deployment Pipeline")

                st.code("""
                Developer
                  ↓
                GitHub
                  ↓
                Docker Build
                  ↓
                Container Registry
                  ↓
                Azure Container Apps
                  ↓
                Production Environment
                """)
                st.write("### 💰 Cost Visibility")

                prompt_tokens = int(
                    len(trace.prompt.split()) * 1.3
                )

                output_tokens = int(
                    len(trace.output_data.split()) * 1.3
                )

                estimated_cost = round(
                    ((prompt_tokens + output_tokens) / 1000) * 0.02,
                    4
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Prompt Tokens",
                        prompt_tokens
                    )

                with col2:
                    st.metric(
                        "Output Tokens",
                        output_tokens
                    )

                with col3:
                    st.metric(
                        "Estimated Cost ($)",
                        estimated_cost
                    )
                st.write("### 🔍 Audit Trail")

                st.code(f"""
                Agent Used:
                {trace.name}

                Execution Time:
                {trace.execution_time}s

                Prompt Size:
                {len(trace.prompt)} Characters

                Input Tokens:
                {trace.input_tokens}

                Output Tokens:
                {trace.output_tokens}

                Estimated Cost:
                ₹{trace.estimated_cost}
                """)

            with st.expander(
                "🛡 Governance X-Ray"
            ):
                st.write("### 📚 Data Lineage")

                st.code(f"""
                Data Sources Used

                ✓ Transcript

                ✓ SAP Knowledge Base

                ✓ Screen Analysis

                ✓ Agent Instructions

                Input Size

                {len(trace.input_data)} Characters
                """)

                st.write("### 🔍 Decision Traceability")

                st.code(f"""
                Agent:
                {trace.name}

                Purpose:
                {trace.purpose}

                Why Invoked:
                {trace.why_called}

                Next Step:
                {trace.next_step}
                """)

                st.write("### 🧠 AI Governance Controls")

                st.code("""
                Model Used:
                GPT-4.1

                Prompt Visible:
                YES

                Input Visible:
                YES

                Output Visible:
                YES

                Audit Available:
                YES
                """)

                st.write("### Human Approval Workflow")

                st.code("""
                Transcript
                      ↓

                AI Draft Generated
                      ↓

                Business Review
                      ↓

                Approve / Reject
                      ↓

                Final BRD
                """)

                st.write("### Compliance Controls")

                st.success("""
                ✓ Prompt Traceability

                ✓ Output Traceability

                ✓ Human Review

                ✓ Cost Tracking

                ✓ Agent Audit Trail

                ✓ Production Monitoring
                """)

                st.write("### Trust Score")

                trust_score = 95

                st.progress(
                    trust_score / 100
                )

                st.metric(
                    "AI Transparency Score",
                    f"{trust_score}%"
                )
    
            st.write("### Next Step")
            st.success(trace.next_step)

            st.write(
                f"Execution Time: {trace.execution_time}s"
            )

            st.write(
                f"Input Tokens: {trace.input_tokens}"
            )

            st.write(
                f"Output Tokens: {trace.output_tokens}"
            )

            st.write(
                f"Estimated Cost: ₹{trace.estimated_cost}"
            )
