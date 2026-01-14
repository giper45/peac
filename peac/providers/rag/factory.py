"""Factory for RAG providers - handles dynamic provider selection"""

from typing import Optional, Dict, Any

from .base import BaseRAGProvider
from .fastembed_provider import FastembedProvider
from .faiss_provider import FaissProvider


class RAGProviderFactory:
    """Factory class to create and manage RAG providers"""
    
    # Default provider if not specified
    DEFAULT_PROVIDER = 'fastembed'
    
    # Available providers
    PROVIDERS = {
        'fastembed': FastembedProvider,
        'faiss': FaissProvider,
    }
    
    @classmethod
    def create(cls, provider_name: Optional[str] = None) -> BaseRAGProvider:
        """
        Create a RAG provider instance
        
        Args:
            provider_name: Name of the provider ('fastembed' or 'faiss')
                          If None, uses DEFAULT_PROVIDER
        
        Returns:
            Instance of the requested RAG provider
        
        Raises:
            ValueError: If provider_name is not recognized
        """
        if provider_name is None:
            provider_name = cls.DEFAULT_PROVIDER
        
        provider_name = provider_name.lower().strip()
        
        if provider_name not in cls.PROVIDERS:
            available = ', '.join(cls.PROVIDERS.keys())
            raise ValueError(
                f"Unknown RAG provider: '{provider_name}'. "
                f"Available providers: {available}"
            )
        
        provider_class = cls.PROVIDERS[provider_name]
        return provider_class()
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Get list of available provider names"""
        return list(cls.PROVIDERS.keys())
    
    @classmethod
    def is_valid_provider(cls, provider_name: str) -> bool:
        """Check if provider name is valid"""
        return provider_name.lower().strip() in cls.PROVIDERS


# Convenience function for single provider instantiation
def get_rag_provider(provider_name: Optional[str] = None) -> BaseRAGProvider:
    """
    Convenience function to get a RAG provider instance
    
    Args:
        provider_name: Name of the provider (default: 'fastembed')
    
    Returns:
        RAG provider instance
    """
    return RAGProviderFactory.create(provider_name)
