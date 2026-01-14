"""
Performance benchmarking suite for PEaC RAG providers.

Compares FastEmbed vs FAISS performance on:
- Peak memory usage (RAM constraint on consumer PCs)
- Query response time (frequent operation)
- Index creation time (one-time cost)
- Disk space (index file size)

Results validate FastEmbed's suitability for general-purpose hardware.
"""
import os
import pytest
import time
import psutil
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

from peac.providers.rag.factory import RAGProviderFactory
from peac.providers.rag.base import BaseRAGProvider


# Test corpus configuration
CORPUS_SIZE = 100  # documents
CORPUS_AVG_SIZE_KB = 10  # average document size
NUM_RUNS = 50  # repetitions for statistical reliability
NUM_QUERIES = 10  # queries per benchmark run


# Test queries for semantic search
TEST_QUERIES = [
    "machine learning algorithms",
    "neural network architectures",
    "natural language processing techniques",
    "computer vision applications",
    "deep learning optimization",
    "reinforcement learning methods",
    "transformer models attention",
    "data preprocessing pipelines",
    "model evaluation metrics",
    "deployment best practices"
]


class PerformanceMetrics:
    """Container for performance measurements"""
    
    def __init__(self):
        self.index_creation_times: List[float] = []
        self.query_response_times: List[float] = []
        self.peak_memory_mb: List[float] = []
        self.index_size_mb: List[float] = []
    
    def add_measurement(
        self,
        index_time: float,
        query_times: List[float],
        peak_mem: float,
        index_size: float
    ):
        """Add a single benchmark run measurement"""
        self.index_creation_times.append(index_time)
        self.query_response_times.extend(query_times)
        self.peak_memory_mb.append(peak_mem)
        self.index_size_mb.append(index_size)
    
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """Calculate statistics across all runs"""
        import statistics
        
        def calc_stats(values: List[float]) -> Dict[str, float]:
            if not values:
                return {"mean": 0, "median": 0, "std": 0, "min": 0, "max": 0}
            return {
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "std": statistics.stdev(values) if len(values) > 1 else 0,
                "min": min(values),
                "max": max(values)
            }
        
        return {
            "index_creation_time_s": calc_stats(self.index_creation_times),
            "query_response_time_ms": calc_stats(
                [t * 1000 for t in self.query_response_times]  # Convert to ms
            ),
            "peak_memory_mb": calc_stats(self.peak_memory_mb),
            "index_size_mb": calc_stats(self.index_size_mb)
        }


def get_memory_usage_mb() -> float:
    """Get current process memory usage in MB"""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)


def get_directory_size_mb(path: str) -> float:
    """Get total size of directory in MB"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)


def benchmark_provider(
    provider_type: str,
    corpus_dir: str,
    num_runs: int = NUM_RUNS
) -> PerformanceMetrics:
    """
    Benchmark a single RAG provider.
    
    Args:
        provider_type: 'fastembed' or 'faiss'
        corpus_dir: Path to document corpus
        num_runs: Number of benchmark repetitions
    
    Returns:
        PerformanceMetrics with aggregated measurements
    """
    metrics = PerformanceMetrics()
    
    print(f"\nBenchmarking {provider_type} provider ({num_runs} runs)...")
    
    for run in range(num_runs):
        # Create temporary directory for this run
        with tempfile.TemporaryDirectory() as temp_dir:
            index_file = os.path.join(temp_dir, "index.json")
            
            # Measure index creation
            mem_before = get_memory_usage_mb()
            
            start_time = time.time()
            provider = RAGProviderFactory.create(provider_type)
            
            # Create index by parsing with force_override
            provider.parse(
                index_path=index_file,
                options={
                    'query': 'test',  # Dummy query for initial index creation
                    'source_folder': corpus_dir,
                    'force_override': True,
                    'chunk_size': 512,
                    'overlap': 50
                }
            )
            index_time = time.time() - start_time
            
            mem_after = get_memory_usage_mb()
            peak_memory = mem_after - mem_before
            
            # Measure index size
            index_size = get_directory_size_mb(temp_dir)
            
            # Measure query response times
            query_times = []
            for query in TEST_QUERIES:
                start_time = time.time()
                results = provider.parse(
                    index_path=index_file,
                    options={
                        'query': query,
                        'top_k': 5,
                        'source_folder': corpus_dir
                    }
                )
                query_time = time.time() - start_time
                query_times.append(query_time)
            
            # Record measurements
            metrics.add_measurement(
                index_time=index_time,
                query_times=query_times,
                peak_mem=peak_memory,
                index_size=index_size
            )
        
        # Progress indicator
        if (run + 1) % 10 == 0:
            print(f"  Completed {run + 1}/{num_runs} runs...")
    
    print(f"Completed {provider_type} benchmarks")
    return metrics


@pytest.fixture(scope="module")
def benchmark_corpus():
    """Generate synthetic corpus for testing"""
    from tests.utils.generate_synthetic_corpus import generate_corpus
    
    corpus_dir = "tests/benchmark_corpus"
    
    # Generate corpus if it doesn't exist
    if not os.path.exists(corpus_dir) or len(os.listdir(corpus_dir)) < CORPUS_SIZE:
        print(f"\nGenerating synthetic corpus ({CORPUS_SIZE} documents)...")
        generate_corpus(corpus_dir, CORPUS_SIZE, CORPUS_AVG_SIZE_KB)
    else:
        print(f"\nUsing existing corpus at {corpus_dir}")
    
    yield corpus_dir
    
    # Cleanup after all tests (optional, comment out to keep corpus)
    # shutil.rmtree(corpus_dir, ignore_errors=True)


class TestRAGPerformance:
    """Performance benchmark tests for RAG providers"""
    
    def test_fastembed_performance(self, benchmark_corpus):
        """Benchmark FastEmbed provider performance"""
        metrics = benchmark_provider("fastembed", benchmark_corpus, num_runs=NUM_RUNS)
        stats = metrics.get_stats()
        
        # Print results
        print("\n" + "="*70)
        print("FastEmbed Performance Results")
        print("="*70)
        print(f"Index Creation Time: {stats['index_creation_time_s']['mean']:.3f}s "
              f"(±{stats['index_creation_time_s']['std']:.3f}s)")
        print(f"Query Response Time: {stats['query_response_time_ms']['mean']:.2f}ms "
              f"(±{stats['query_response_time_ms']['std']:.2f}ms)")
        print(f"Peak Memory Usage: {stats['peak_memory_mb']['mean']:.2f}MB "
              f"(±{stats['peak_memory_mb']['std']:.2f}MB)")
        print(f"Index Size: {stats['index_size_mb']['mean']:.2f}MB "
              f"(±{stats['index_size_mb']['std']:.2f}MB)")
        print("="*70)
        
        # Assertions for reasonable performance (adjust based on hardware)
        assert stats['index_creation_time_s']['mean'] < 60.0, "Index creation too slow"
        assert stats['query_response_time_ms']['mean'] < 1000.0, "Query response too slow"
        assert stats['peak_memory_mb']['mean'] < 2000.0, "Memory usage too high"
    
    def test_faiss_performance(self, benchmark_corpus):
        """Benchmark FAISS provider performance"""
        try:
            metrics = benchmark_provider("faiss", benchmark_corpus, num_runs=NUM_RUNS)
            stats = metrics.get_stats()
            
            # Print results
            print("\n" + "="*70)
            print("FAISS Performance Results")
            print("="*70)
            print(f"Index Creation Time: {stats['index_creation_time_s']['mean']:.3f}s "
                  f"(±{stats['index_creation_time_s']['std']:.3f}s)")
            print(f"Query Response Time: {stats['query_response_time_ms']['mean']:.2f}ms "
                  f"(±{stats['query_response_time_ms']['std']:.2f}ms)")
            print(f"Peak Memory Usage: {stats['peak_memory_mb']['mean']:.2f}MB "
                  f"(±{stats['peak_memory_mb']['std']:.2f}MB)")
            print(f"Index Size: {stats['index_size_mb']['mean']:.2f}MB "
                  f"(±{stats['index_size_mb']['std']:.2f}MB)")
            print("="*70)
            
        except ImportError:
            pytest.skip("FAISS not installed")
    
    def test_compare_providers(self, benchmark_corpus):
        """Compare FastEmbed vs FAISS performance"""
        print("\n" + "="*70)
        print("RAG Provider Performance Comparison")
        print("="*70)
        
        # Benchmark FastEmbed
        fastembed_metrics = benchmark_provider("fastembed", benchmark_corpus, num_runs=NUM_RUNS)
        fastembed_stats = fastembed_metrics.get_stats()
        
        # Try to benchmark FAISS
        try:
            faiss_metrics = benchmark_provider("faiss", benchmark_corpus, num_runs=NUM_RUNS)
            faiss_stats = faiss_metrics.get_stats()
            has_faiss = True
        except ImportError:
            print("\nFAISS not available, showing FastEmbed results only")
            has_faiss = False
            faiss_stats = None
        
        # Print comparison table
        print("\n" + "="*70)
        print(f"{'Metric':<40} {'FastEmbed':<15} {'FAISS':<15}")
        print("="*70)
        
        def format_comparison(metric_name, fastembed_val, faiss_val=None):
            fe_str = f"{fastembed_val['mean']:.2f}±{fastembed_val['std']:.2f}"
            if faiss_val and has_faiss:
                f_str = f"{faiss_val['mean']:.2f}±{faiss_val['std']:.2f}"
                print(f"{metric_name:<40} {fe_str:<15} {f_str:<15}")
            else:
                print(f"{metric_name:<40} {fe_str:<15} {'N/A':<15}")
        
        format_comparison(
            "Index Creation Time (s)",
            fastembed_stats['index_creation_time_s'],
            faiss_stats['index_creation_time_s'] if has_faiss else None
        )
        format_comparison(
            "Query Response Time (ms)",
            fastembed_stats['query_response_time_ms'],
            faiss_stats['query_response_time_ms'] if has_faiss else None
        )
        format_comparison(
            "Peak Memory Usage (MB)",
            fastembed_stats['peak_memory_mb'],
            faiss_stats['peak_memory_mb'] if has_faiss else None
        )
        format_comparison(
            "Index Size (MB)",
            fastembed_stats['index_size_mb'],
            faiss_stats['index_size_mb'] if has_faiss else None
        )
        
        print("="*70)
        
        # Calculate improvement percentages if FAISS available
        if has_faiss:
            print("\nPerformance Comparison (FastEmbed vs FAISS):")
            
            mem_diff = ((fastembed_stats['peak_memory_mb']['mean'] - 
                        faiss_stats['peak_memory_mb']['mean']) / 
                       faiss_stats['peak_memory_mb']['mean'] * 100)
            
            time_diff = ((fastembed_stats['query_response_time_ms']['mean'] - 
                         faiss_stats['query_response_time_ms']['mean']) / 
                        faiss_stats['query_response_time_ms']['mean'] * 100)
            
            index_diff = ((fastembed_stats['index_creation_time_s']['mean'] - 
                          faiss_stats['index_creation_time_s']['mean']) / 
                         faiss_stats['index_creation_time_s']['mean'] * 100)
            
            print(f"  Memory Usage: {abs(mem_diff):.1f}% {'lower' if mem_diff < 0 else 'higher'}")
            print(f"  Query Time: {abs(time_diff):.1f}% {'faster' if time_diff < 0 else 'slower'}")
            print(f"  Index Creation: {abs(index_diff):.1f}% {'faster' if index_diff < 0 else 'slower'}")
        
        print("\n" + "="*70)


def pytest_addoption(parser):
    """Add custom pytest options"""
    parser.addoption(
        "--run-faiss",
        action="store_true",
        default=False,
        help="Run FAISS performance benchmarks"
    )


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
