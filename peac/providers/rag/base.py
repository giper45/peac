"""Base abstract class for RAG providers"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseRAGProvider(ABC):
    """Abstract base class for RAG (Retrieval-Augmented Generation) providers"""
    
    def __init__(self):
        """Initialize the RAG provider"""
        pass
    
    @abstractmethod
    def parse(self, index_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Parse RAG request and return relevant documents
        
        Args:
            index_path: Path to the vector index file/directory
            options: Dictionary containing:
                - query: Search query for RAG retrieval
                - source_folder: Folder/file to embed if index doesn't exist
                - top_k: Number of top results to return (default: 5)
                - chunk_size: Size of text chunks for embedding (default: 512)
                - overlap: Overlap between chunks (default: 50)
                - force_override: Force recreation of index (default: False)
                - embedding_model: Model name for embedding
                - Additional provider-specific params in 'provider_config'
        
        Returns:
            Retrieved and ranked text content
        """
        pass
    
    @abstractmethod
    def apply_filter(self, text: str, filter_regex: str) -> str:
        """
        Apply regex filter to retrieved text
        
        Args:
            text: Retrieved text content
            filter_regex: Regex pattern to match lines
            
        Returns:
            Filtered text content
        """
        pass
    
    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Compute cosine similarity between two vectors"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a ** 2 for a in vec1) ** 0.5
        norm2 = sum(b ** 2 for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
