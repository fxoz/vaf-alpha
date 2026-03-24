from abc import ABC, abstractmethod


class TtsProvider(ABC):
    @abstractmethod
    def say(self, text: str) -> None:
        raise NotImplementedError()
