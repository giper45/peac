"""RAG providers package - supports multiple vector search backends"""

from .factory import RAGProviderFactory, get_rag_provider
from .base import BaseRAGProvider
from .fastembed_provider import FastembedProvider
from .faiss_provider import FaissProvider

# Backward compatibility: Import from legacy module

__all__ = [
    'RAGProviderFactory',
    'get_rag_provider',
    'BaseRAGProvider',
    'FastembedProvider',
    'FaissProvider',
    'RagProvider',  # Legacy support
]
