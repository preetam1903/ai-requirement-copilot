from ai_xray.components.agent_card import render_agent_card

def render_xray(trace_store):

    traces = trace_store.get_traces()

    for trace in traces:
        render_agent_card(trace)
