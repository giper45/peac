from abc import ABC, abstractmethod

class FileProvider(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> str:
        pass