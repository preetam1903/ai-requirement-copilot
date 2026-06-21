import streamlit as st

def render_agent_card(trace):

    with st.expander(f"🔍 {trace.name}"):

        st.write("### Purpose")
        st.write(trace.purpose)

        st.write("### Why Called")
        st.write(trace.why_called)

        st.write("### Input")
        st.write(trace.input_data)

        st.write("### Prompt")
        st.code(trace.prompt)

        st.write("### Output")
        st.write(trace.output_data)

        st.write("### Next Step")
        st.write(trace.next_step)

        st.write("### Tokens")
        st.write(
            f"Input: {trace.input_tokens} | "
            f"Output: {trace.output_tokens}"
        )

        st.write(
            f"Estimated Cost: ₹{trace.estimated_cost:.2f}"
        )
