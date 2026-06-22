import streamlit as st

def render_xray(trace_store):

    traces = trace_store.get_traces()

    for trace in traces:

        with st.expander(
            f"🔍 {trace.name}"
        ):

            st.write("### Purpose")
            st.write(trace.purpose)

            st.write("### Why Called")
            st.write(trace.why_called)

            st.write("### Input")
            st.text_area(
                "Input",
                trace.input_data,
                height=200
            )

            st.write("### Prompt")
            st.text_area(
                "Prompt",
                trace.prompt,
                height=300
            )

            st.write("### Output")
            st.text_area(
                "Output",
                trace.output_data,
                height=250
            )

            with st.expander(
                "🧠 Behind The Scenes - LLM Processing"
            ):

                st.markdown("""
            ### Step 1 - Input Received

            The agent receives business context, transcript and supporting information.

            ⬇️

            ### Step 2 - Tokenization

            The LLM breaks the text into smaller pieces called tokens.

            Example:

            Current SAP supports 9 digits

            ↓

            Current | SAP | supports | 9 | digits

            ⬇️

            ### Step 3 - Prompt Assembly

            The system combines:

            • System Instructions

            • Agent Prompt

            • Meeting Context

            • Screen Analysis

            into one final prompt.

            ⬇️

            ### Step 4 - LLM Processing

            The model analyzes:

            • Business intent

            • Requirements

            • SAP context

            • Change request

            ⬇️

            ### Step 5 - Token Prediction

            The model predicts the most likely next words.

            Example:

            "The system"

            ↓

            shall (91%)

            must (5%)

            will (3%)

            ⬇️

            ### Step 6 - Response Generation

            The predicted tokens are combined into a BRD or Requirements document.

            ⬇️

            ### Step 7 - Agent Output

            The result is returned to the next agent.
            """)
            with st.expander(
                "🧠 Behind The Scenes"
            ):

                st.markdown("""
            ### What Happened?

            1. Input converted into tokens

            2. Prompt combined with context

            3. LLM analyzed instructions

            4. Next words predicted

            5. Response generated

            6. Output returned to agent
            """)

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
