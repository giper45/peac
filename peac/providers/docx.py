from .base import FileProvider
from docx import Document

class DocxProvider(FileProvider):
    def parse(self, file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])