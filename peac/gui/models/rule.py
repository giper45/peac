from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any, Literal

RuleType = Literal["local", "web", "rag"]


@dataclass
class RuleData:
    type: RuleType
    name: str = ""
    preamble: str = ""

    # local
    source: Optional[str] = None
    recursive: bool = False
    extension: Optional[str] = None
    filter: Optional[str] = None

    # web
    url: Optional[str] = None
    xpath: Optional[str] = None

    # rag
    faiss_file: Optional[str] = None
    source_folder: Optional[str] = None  # Folder to embed if FAISS doesn't exist
    query: Optional[str] = None
    embedding_model: str = "all-MiniLM-L6-v2"  # Default embedding model
    force_override: bool = False  # Force recreate FAISS index
    top_k: Optional[int] = None
    chunk_size: Optional[int] = None
    overlap: Optional[int] = None
    filter_regex: Optional[str] = None

    def to_yaml_dict(self) -> Optional[Dict[str, Any]]:
        """Serialize only meaningful fields (no empties)."""
        out: Dict[str, Any] = {}

        # preamble + name are optional and depend on how you want YAML shaped.
        # For now we keep them out unless you want them in schema.

        if self.type == "local":
            if self.source:
                out["source"] = self.source
            if self.recursive:
                out["recursive"] = self.recursive
            if self.extension:
                out["extension"] = self.extension
            if self.filter:
                out["filter"] = self.filter

        elif self.type == "web":
            if self.url:
                out["source"] = self.url
            if self.xpath:
                out["xpath"] = self.xpath

        elif self.type == "rag":
            if self.faiss_file:
                out["faiss_file"] = self.faiss_file
            if self.source_folder:
                out["source"] = self.source_folder
            if self.query:
                out["query"] = self.query
            if self.embedding_model and self.embedding_model != "all-MiniLM-L6-v2":  # Only save if non-default
                out["embedding_model"] = self.embedding_model
            if self.force_override:
                out["force_override"] = self.force_override
            if isinstance(self.top_k, int):
                out["top_k"] = self.top_k
            if isinstance(self.chunk_size, int):
                out["chunk_size"] = self.chunk_size
            if isinstance(self.overlap, int):
                out["overlap"] = self.overlap
            if self.filter_regex:
                out["filter"] = self.filter_regex

        return out or None
