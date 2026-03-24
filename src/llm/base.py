from abc import ABC, abstractmethod


class LlmProvider(ABC):
    @abstractmethod
    def respond(self, text: str) -> str:
        raise NotImplementedError()
