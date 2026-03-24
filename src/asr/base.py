from abc import ABC, abstractmethod


class AsrProvider(ABC):
    @abstractmethod
    def transcribe(self, file_path: str) -> str:
        raise NotImplementedError()
