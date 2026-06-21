class TraceStore:

    def __init__(self):
        self.traces = []

    def add_trace(self, trace):
        self.traces.append(trace)

    def get_traces(self):
        return self.traces

    def clear(self):
        self.traces = []
