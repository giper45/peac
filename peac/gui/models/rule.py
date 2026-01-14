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
    index_path: Optional[str] = None  # Path to vector index (renamed from faiss_file)
    faiss_file: Optional[str] = None  # Legacy field for backward compatibility
    source_folder: Optional[str] = None  # Folder to embed if index doesn't exist
    query: Optional[str] = None
    embedding_model: str = "BAAI/bge-small-en-v1.5"  # Default embedding model
    provider: str = "fastembed"  # RAG provider: 'fastembed' or 'faiss'
    provider_config: Optional[Dict[str, Any]] = None  # Provider-specific configuration
    force_override: bool = False  # Force recreate index
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
            # Support both new index_path and legacy faiss_file
            index_path = self.index_path or self.faiss_file
            if index_path:
                out["index_path"] = index_path
            if self.source_folder:
                out["source_folder"] = self.source_folder
            if self.query:
                out["query"] = self.query
            if self.provider and self.provider != "fastembed":  # Only save if not default
                out["provider"] = self.provider
            if self.embedding_model and self.embedding_model != "BAAI/bge-small-en-v1.5":  # Only save if non-default
                out["embedding_model"] = self.embedding_model
            if self.provider_config:  # Only save if not empty
                out["provider_config"] = self.provider_config
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
