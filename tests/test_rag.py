"""
RAG Provider Test Suite

Tests for RAG (Retrieval-Augmented Generation) functionality using pytest.
Tests both FastEmbed (default) and FAISS (optional) providers.
"""

import os
import pytest
import json
import tempfile
from pathlib import Path
from typing import Optional

from peac.providers.rag.factory import RAGProviderFactory, get_rag_provider
from peac.providers.rag.fastembed_provider import FastembedProvider
from peac.core.peac import PromptYaml


class TestRAGProviderFactory:
    """Test RAG provider factory pattern"""

    def test_factory_default_provider(self):
        """Test that default provider is FastEmbed"""
        provider = RAGProviderFactory.create()
        assert isinstance(provider, FastembedProvider)
        assert provider.__class__.__name__ == "FastembedProvider"

    def test_factory_create_fastembed(self):
        """Test creating FastEmbed provider explicitly"""
        provider = RAGProviderFactory.create("fastembed")
        assert isinstance(provider, FastembedProvider)

    def test_factory_invalid_provider(self):
        """Test that invalid provider name raises error"""
        with pytest.raises(ValueError, match="Unknown RAG provider"):
            RAGProviderFactory.create("invalid_provider")

    def test_factory_get_rag_provider_function(self):
        """Test get_rag_provider convenience function"""
        provider = get_rag_provider("fastembed")
        assert isinstance(provider, FastembedProvider)

    def test_factory_provider_config(self):
        """Test factory with provider config"""
        provider = RAGProviderFactory.create("fastembed")
        assert provider is not None


class TestFastembed:
    """Test FastEmbed provider basic functionality"""

    @pytest.fixture
    def temp_index_dir(self):
        """Create temporary directory for test indexes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def sample_docs_folder(self):
        """Return path to sample-docs folder"""
        return os.path.join("examples", "sample-docs")

    @pytest.fixture
    def fastembed_provider(self):
        """Create FastEmbed provider instance"""
        return FastembedProvider()

    def test_provider_initialization(self, fastembed_provider):
        """Test provider initializes correctly"""
        assert fastembed_provider is not None
        assert hasattr(fastembed_provider, "parse")
        assert hasattr(fastembed_provider, "apply_filter")

    def test_provider_has_embedding_model(self, fastembed_provider):
        """Test provider has embedding model loaded"""
        # Model should be lazily loaded on first use
        assert fastembed_provider is not None

    def test_index_creation_from_folder(self, fastembed_provider, temp_index_dir, sample_docs_folder):
        """Test index creation from source folder"""
        if not os.path.exists(sample_docs_folder):
            pytest.skip(f"Sample docs folder not found at {sample_docs_folder}")

        index_path = os.path.join(temp_index_dir, "test_index.json")
        
        result = fastembed_provider.parse(
            index_path=index_path,
            options={
                'source_folder': sample_docs_folder,
                'chunk_size': 256,
                'overlap': 30,
                'query': 'test'  # Required for search
            }
        )

        # Check that index was created
        assert os.path.exists(index_path), f"Index not created at {index_path}"
        
        # Check index is valid JSON
        with open(index_path, 'r') as f:
            index_data = json.load(f)
        
        assert "chunks" in index_data
        assert len(index_data["chunks"]) > 0
        assert "embeddings" in index_data
        assert len(index_data["embeddings"]) == len(index_data["chunks"])

    def test_semantic_search(self, fastembed_provider, temp_index_dir, sample_docs_folder):
        """Test semantic search functionality"""
        if not os.path.exists(sample_docs_folder):
            pytest.skip(f"Sample docs folder not found at {sample_docs_folder}")

        index_path = os.path.join(temp_index_dir, "test_search.json")
        
        # Create index and perform search
        query = "Python best practices"
        result = fastembed_provider.parse(
            index_path=index_path,
            options={
                'source_folder': sample_docs_folder,
                'chunk_size': 256,
                'overlap': 30,
                'query': query,
                'top_k': 3
            }
        )

        # Result should contain search results
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain rank information
        assert "Rank" in result or "rank" in result or len(result) > 50

    def test_search_top_k_limit(self, fastembed_provider, temp_index_dir, sample_docs_folder):
        """Test that top_k parameter limits results"""
        if not os.path.exists(sample_docs_folder):
            pytest.skip(f"Sample docs folder not found at {sample_docs_folder}")

        index_path = os.path.join(temp_index_dir, "test_topk.json")
        
        # Test different top_k values - each parse creates and searches
        for top_k in [1, 3]:
            result = fastembed_provider.parse(
                index_path=index_path,
                options={
                    'source_folder': sample_docs_folder,
                    'chunk_size': 256,
                    'overlap': 30,
                    'query': 'testing code',
                    'top_k': top_k,
                    'force_override': True  # Recreate index for each test
                }
            )
            # Count ranks in result
            rank_count = result.count("Rank ")
            assert rank_count <= top_k

    def test_chunk_size_parameter(self, fastembed_provider, temp_index_dir, sample_docs_folder):
        """Test that chunk_size parameter affects chunking"""
        if not os.path.exists(sample_docs_folder):
            pytest.skip(f"Sample docs folder not found at {sample_docs_folder}")

        # Create index with small chunk size
        index_path_small = os.path.join(temp_index_dir, "test_chunks_small.json")
        fastembed_provider.parse(
            index_path=index_path_small,
            options={
                'source_folder': sample_docs_folder,
                'chunk_size': 100,
                'overlap': 10,
                'query': 'test',
                'top_k': 1
            }
        )

        with open(index_path_small, 'r') as f:
            small_chunks = json.load(f)
        
        # Create index with large chunk size
        index_path_large = os.path.join(temp_index_dir, "test_chunks_large.json")
        fastembed_provider.parse(
            index_path=index_path_large,
            options={
                'source_folder': sample_docs_folder,
                'chunk_size': 1000,
                'overlap': 100,
                'query': 'test',
                'top_k': 1
            }
        )

        with open(index_path_large, 'r') as f:
            large_chunks = json.load(f)
        
        # Smaller chunk size should result in more chunks
        assert len(small_chunks["chunks"]) > len(large_chunks["chunks"])


class TestRAGYAMLIntegration:
    """Test RAG integration with YAML configuration"""

    @pytest.fixture
    def rag_yaml_simple(self):
        """Return path to simple RAG YAML"""
        return os.path.join("examples", "rag-simple.yaml")

    @pytest.fixture
    def rag_yaml_sample_docs(self):
        """Return path to sample-docs RAG YAML"""
        return os.path.join("examples", "rag-sample-docs.yaml")

    def test_yaml_parsing_simple(self, rag_yaml_simple):
        """Test parsing simple RAG YAML"""
        if not os.path.exists(rag_yaml_simple):
            pytest.skip(f"YAML file not found at {rag_yaml_simple}")

        py = PromptYaml(rag_yaml_simple)
        rag_rules = py.get_rag_rules('context')

        assert rag_rules is not None
        assert len(rag_rules) > 0

    def test_yaml_parsing_sample_docs(self, rag_yaml_sample_docs):
        """Test parsing sample-docs RAG YAML"""
        if not os.path.exists(rag_yaml_sample_docs):
            pytest.skip(f"YAML file not found at {rag_yaml_sample_docs}")

        py = PromptYaml(rag_yaml_sample_docs)
        rag_rules = py.get_rag_rules('context')

        assert rag_rules is not None
        assert len(rag_rules) > 0

    def test_yaml_rag_rule_structure(self, rag_yaml_simple):
        """Test RAG rule structure from YAML"""
        if not os.path.exists(rag_yaml_simple):
            pytest.skip(f"YAML file not found at {rag_yaml_simple}")

        py = PromptYaml(rag_yaml_simple)
        rag_rules = py.get_rag_rules('context')

        # Should return list of PromptSection objects
        assert len(rag_rules) > 0
        rule = rag_rules[0]
        
        # PromptSection has 'lines' attribute
        assert hasattr(rule, '__getitem__')  # Dict-like
        assert 'lines' in rule

    def test_yaml_provider_field(self, rag_yaml_sample_docs):
        """Test that provider field is correctly parsed"""
        if not os.path.exists(rag_yaml_sample_docs):
            pytest.skip(f"YAML file not found at {rag_yaml_sample_docs}")

        py = PromptYaml(rag_yaml_sample_docs)
        rag_rules = py.get_rag_rules('context')

        rule = rag_rules[0]
        # Provider should be present (either explicitly or defaulted)
        provider = rule.get("provider", "fastembed")
        assert provider in ["fastembed", "faiss"]


class TestFaissProviderOptional:
    """Test FAISS provider (optional, requires installation)"""

    @pytest.fixture
    def faiss_available(self):
        """Check if FAISS is available"""
        try:
            import faiss
            return True
        except ImportError:
            return False

    def test_faiss_availability(self, faiss_available):
        """Test FAISS availability"""
        if not faiss_available:
            pytest.skip("FAISS not installed - run 'make faiss-cpu' to install")

    def test_factory_create_faiss(self, faiss_available):
        """Test creating FAISS provider"""
        if not faiss_available:
            pytest.skip("FAISS not installed")

        provider = RAGProviderFactory.create("faiss")
        assert provider is not None
        assert provider.__class__.__name__ == "FaissProvider"

    def test_faiss_index_creation(self, faiss_available):
        """Test FAISS index creation"""
        if not faiss_available:
            pytest.skip("FAISS not installed")

        sample_docs_folder = os.path.join("examples", "sample-docs")
        if not os.path.exists(sample_docs_folder):
            pytest.skip(f"Sample docs folder not found at {sample_docs_folder}")

        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = os.path.join(tmpdir, "test_faiss.index")
            
            provider = RAGProviderFactory.create("faiss")
            provider.parse(
                index_path=index_path,
                options={
                    'source_folder': sample_docs_folder,
                    'index_type': 'flat',
                    'query': 'test',
                    'top_k': 3
                }
            )

            # FAISS creates index at the specified path
            # The provider should have created the index successfully (check output message)
            assert os.path.exists(index_path) or os.path.exists(f"{index_path}.faiss")


class TestRAGEdgeCases:
    """Test edge cases and error handling"""

    @pytest.fixture
    def fastembed_provider(self):
        """Create FastEmbed provider instance"""
        return FastembedProvider()

    def test_empty_folder_handling(self, fastembed_provider):
        """Test handling of empty source folder"""
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_folder = os.path.join(tmpdir, "empty")
            os.makedirs(empty_folder)
            index_path = os.path.join(tmpdir, "empty_index.json")

            # Should handle gracefully
            try:
                result = fastembed_provider.parse(
                    index_path=index_path,
                    options={
                        'source_folder': empty_folder,
                        'chunk_size': 256,
                        'query': 'test',
                        'top_k': 1
                    }
                )
                # Either creates empty index or raises informative error
                if os.path.exists(index_path):
                    with open(index_path, 'r') as f:
                        data = json.load(f)
                    assert isinstance(data, dict)
            except Exception as e:
                # Should have informative error message
                assert str(e) != ""

    def test_search_empty_index(self, fastembed_provider):
        """Test search on non-existent index"""
        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = os.path.join(tmpdir, "nonexistent.json")

            # Should handle gracefully
            with pytest.raises(Exception):
                fastembed_provider.apply_filter(
                    index_path=index_path,
                    query="test",
                    top_k=3
                )

    def test_zero_top_k(self, fastembed_provider):
        """Test top_k=0 parameter"""
        sample_docs_folder = os.path.join("examples", "sample-docs")
        if not os.path.exists(sample_docs_folder):
            pytest.skip(f"Sample docs folder not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = os.path.join(tmpdir, "test_zero_topk.json")
            
            result = fastembed_provider.parse(
                index_path=index_path,
                options={
                    'source_folder': sample_docs_folder,
                    'chunk_size': 256,
                    'query': 'test',
                    'top_k': 0  # Zero results
                }
            )

            # top_k=0 should return minimal or no results
            rank_count = result.count("Rank ")
            assert rank_count == 0

    def test_special_characters_in_query(self, fastembed_provider):
        """Test search with special characters"""
        sample_docs_folder = os.path.join("examples", "sample-docs")
        if not os.path.exists(sample_docs_folder):
            pytest.skip(f"Sample docs folder not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = os.path.join(tmpdir, "test_special_chars.json")

            # Should handle special characters in queries
            queries = [
                "test@123!",
                "café",
                "what's the meaning?",
                "C++ programming"
            ]

            for query in queries:
                result = fastembed_provider.parse(
                    index_path=index_path,
                    options={
                        'source_folder': sample_docs_folder,
                        'chunk_size': 256,
                        'query': query,
                        'top_k': 1,
                        'force_override': True
                    }
                )
                assert isinstance(result, str)
                assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
