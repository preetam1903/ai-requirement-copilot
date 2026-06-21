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
            st.text(trace.input_data)

            st.write("### Prompt")
            st.code(trace.prompt)

            st.write("### Output")
            st.text(trace.output_data)

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
