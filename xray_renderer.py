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
            with st.expander(
                "🧠 Prompt Engineering X-Ray"
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

                st.write("### Sample Input")

                sample_text = trace.input_data[:120]

                st.info(sample_text)

                st.write("### Sample Tokens")

                tokens = sample_text.split()[:15]

                st.write("### Approximate Token Count")

                approx_tokens = len(sample_text.split())

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
                st.write("### 🧠 Neural Network X-Ray")

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
                st.write("### Attention Mechanism")

                st.code("""
                Postal Code
                        ↕
                Customer Address
                        ↕
                Invoice Processing
                        ↕
                Communication
                """)

                st.info("""
                The attention mechanism helps the model determine which words and concepts are most relevant when generating the response.
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
