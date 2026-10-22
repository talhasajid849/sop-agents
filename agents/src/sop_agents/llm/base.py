from abc import ABC, abstractmethod
from pydantic import BaseModel


class LLMResponse(BaseModel):
    """What every LLM clinet return: the answer plus the cost of getting it."""

    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float

class LLMClient(ABC):
    """The shared shape of the every client: fake, gemini, claude. """

    @abstractmethod
    def complete(self, prompt: str) -> LLMResponse:
        """Send a prompt, get a reponse."""