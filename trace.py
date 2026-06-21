from dataclasses import dataclass

@dataclass
class AgentTrace:
    name: str
    purpose: str
    why_called: str
    input_data: str
    prompt: str
    output_data: str
    next_step: str
    execution_time: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
