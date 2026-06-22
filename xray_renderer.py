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
