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
            st.write("### Mission")

            st.info(
                trace.purpose
            )

            st.write("### Why was I Invoked")
            st.write(trace.why_called)

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

                st.markdown("""
            ### AI Processing Flow

            Transcript
            ⬇️
            Tokenization
            ⬇️
            Prompt Assembly
            ⬇️
            LLM Processing
            ⬇️
            Response Generation
            ⬇️
            Agent Output
            """)

                

            

                st.metric(
                    "Tokens",
                    approx_tokens
                )
                estimated_cost = round(
                    approx_tokens * 0.00002,
                    4
                )

                st.metric(
                    "Estimated Cost ($)",
                    estimated_cost
                )

                st.success(" | ".join(tokens))

                st.write("### Prompt Size")

                st.metric(
                    "Characters",
                    len(trace.prompt)
                )
                st.write("### Prompt Statistics")

                prompt_chars = len(trace.prompt)

                prompt_words = len(
                    trace.prompt.split()
                )

                approx_tokens = int(
                    prompt_words * 1.3
                )

                st.metric(
                    "Prompt Characters",
                    prompt_chars
                )

                st.metric(
                    "Prompt Words",
                    prompt_words
                )

                st.metric(
                    "Approx Tokens",
                    approx_tokens
                )
                st.write("### Generated Output Size")

                st.metric(
                    "Characters",
                    len(trace.output_data)
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


                st.write("### Prompt Growth Analysis")

                raw_size = len(trace.input_data)

                final_size = len(trace.prompt)

                growth = round(
                    ((final_size - raw_size) / max(raw_size,1)) * 100,
                    1
                )

                st.metric(
                    "Prompt Expansion",
                    f"{growth}%"
                )

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
            Neural Network Layers
                    ↓
            Attention Mechanism
                    ↓
            Token Prediction
                    ↓
            Generated Response
            """)

                st.info("""
            The LLM does not understand words directly.

            Each word is converted into numbers called embeddings.

            These embeddings are processed through multiple neural network layers to identify patterns and relationships.
            """)

                sample_words = trace.input_data.split()[:5]

                st.write("### Example Embeddings")

                for word in sample_words:

                    st.code(
                        f"{word} → [0.24, -0.91, 0.67, 0.11, ...]"
                    )

                st.write("### Attention Heatmap")

                st.code("""
            Customer      ██████████
            Postal Code   ████████
            Address       ███████
            Invoice       █████
            Country       ███
            """)

                st.info("""
            The attention mechanism helps the model determine which words and concepts are most relevant when generating the response.
            """)

            with st.expander(
                "🏭 Production X-Ray"
            ):

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
                st.write("### Data Transparency")

                st.code(f"""
                Data Sources Used

                ✓ Transcript

                ✓ SAP Knowledge Base

                ✓ Screen Analysis

                ✓ Agent Instructions

                Input Size

                {len(trace.input_data)} Characters
                """)

                st.write("### AI Decision Trace")

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

                st.write("### Model Governance")

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
