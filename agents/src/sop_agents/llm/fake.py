import time

from sop_agents.llm.base import LLMClient, LLMResponse


class FakeLLM(LLMClient):
    """A free pretend AI. It always gives the same answer. Used for testing. """

    def __init__(self, answer: str):
        self.answer = answer

    def complete(self, prompt: str) -> LLMResponse:
        start = time.perf_counter()
        text = self.answer
        latency_ms = (time.perf_counter() - start) * 1000
        return LLMResponse(
            text=text,
            model="fake",
            input_tokens=len(prompt.split()),
            output_tokens=len(text.split()),
            latency_ms=latency_ms,
        )