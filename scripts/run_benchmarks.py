#!/usr/bin/env python3
"""
Automated benchmark runner for PEaC RAG providers.

Generates synthetic corpus, runs performance benchmarks, and exports
results to CSV and LaTeX table formats for paper integration.
"""
import os
import sys
import json
import csv
import subprocess
from pathlib import Path
from datetime import datetime


def generate_corpus():
    """Generate synthetic document corpus"""
    print("="*70)
    print("Step 1: Generating Synthetic Document Corpus")
    print("="*70)
    
    from tests.utils.generate_synthetic_corpus import generate_corpus
    
    corpus_dir = "tests/benchmark_corpus"
    generate_corpus(corpus_dir, num_documents=100, avg_size_kb=10)
    
    return corpus_dir


def run_benchmarks():
    """Execute performance benchmarks"""
    print("\n" + "="*70)
    print("Step 2: Running Performance Benchmarks")
    print("="*70)
    
    # Run pytest with performance tests
    result = subprocess.run(
        ["poetry", "run", "pytest", "tests/test_performance.py", "-v", "-s", "--tb=short"],
        capture_output=False,
        text=True
    )
    
    return result.returncode == 0


def extract_results_from_output():
    """
    Run benchmarks and capture output for CSV export.
    This is a simplified version - in production, you'd parse pytest output
    or use pytest plugins for structured output.
    """
    print("\n" + "="*70)
    print("Step 3: Extracting Results")
    print("="*70)
    
    # Run with JSON output
    result = subprocess.run(
        ["poetry", "run", "pytest", "tests/test_performance.py::TestRAGPerformance::test_compare_providers", 
         "-v", "-s", "--tb=short"],
        capture_output=True,
        text=True
    )
    
    # Parse output (simplified - in production use proper pytest hooks)
    output = result.stdout
    
    # For now, create sample results structure
    # In production, these would be parsed from actual test output
    results = {
        "fastembed": {
            "index_creation_time_s": {"mean": 0.0, "std": 0.0},
            "query_response_time_ms": {"mean": 0.0, "std": 0.0},
            "peak_memory_mb": {"mean": 0.0, "std": 0.0},
            "index_size_mb": {"mean": 0.0, "std": 0.0}
        }
    }
    
    return results


def export_to_csv(results: dict, output_path: str = "benchmark_results.csv"):
    """Export benchmark results to CSV"""
    print(f"\nExporting results to {output_path}...")
    
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header
        writer.writerow([
            "Provider",
            "Index Creation Time (s) Mean",
            "Index Creation Time (s) Std",
            "Query Response Time (ms) Mean",
            "Query Response Time (ms) Std",
            "Peak Memory (MB) Mean",
            "Peak Memory (MB) Std",
            "Index Size (MB) Mean",
            "Index Size (MB) Std"
        ])
        
        # Data rows
        for provider, metrics in results.items():
            writer.writerow([
                provider.upper(),
                f"{metrics['index_creation_time_s']['mean']:.3f}",
                f"{metrics['index_creation_time_s']['std']:.3f}",
                f"{metrics['query_response_time_ms']['mean']:.2f}",
                f"{metrics['query_response_time_ms']['std']:.2f}",
                f"{metrics['peak_memory_mb']['mean']:.2f}",
                f"{metrics['peak_memory_mb']['std']:.2f}",
                f"{metrics['index_size_mb']['mean']:.2f}",
                f"{metrics['index_size_mb']['std']:.2f}"
            ])
    
    print(f"Results exported to {output_path}")


def generate_latex_table(results: dict, output_path: str = "benchmark_table.tex"):
    """Generate LaTeX table for paper"""
    print(f"\nGenerating LaTeX table at {output_path}...")
    
    latex = r"""\begin{table}[htbp]
\centering
\caption{RAG Provider Performance Comparison on General-Purpose Hardware}
\label{tab:rag-performance}
\begin{tabular}{lcccc}
\toprule
\textbf{Provider} & \textbf{Memory (MB)} & \textbf{Query Time (ms)} & \textbf{Index Time (s)} & \textbf{Index Size (MB)} \\
\midrule
"""
    
    for provider, metrics in results.items():
        latex += f"{provider.upper()} & "
        latex += f"{metrics['peak_memory_mb']['mean']:.1f}$\\pm${metrics['peak_memory_mb']['std']:.1f} & "
        latex += f"{metrics['query_response_time_ms']['mean']:.1f}$\\pm${metrics['query_response_time_ms']['std']:.1f} & "
        latex += f"{metrics['index_creation_time_s']['mean']:.2f}$\\pm${metrics['index_creation_time_s']['std']:.2f} & "
        latex += f"{metrics['index_size_mb']['mean']:.1f}$\\pm${metrics['index_size_mb']['std']:.1f} \\\\\n"
    
    latex += r"""\bottomrule
\end{tabular}
\begin{tablenotes}
\small
\item Performance measured over 50 runs on a 100-document corpus (avg. 10KB/doc).
\item Hardware: [INSERT YOUR SPECS] (e.g., Apple M1, 16GB RAM)
\item Values shown as mean $\pm$ standard deviation.
\end{tablenotes}
\end{table}
"""
    
    with open(output_path, 'w') as f:
        f.write(latex)
    
    print(f"LaTeX table generated at {output_path}")


def main():
    """Main benchmark execution workflow"""
    print("="*70)
    print("PEaC RAG Provider Performance Benchmark Suite")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Generate corpus
    corpus_dir = generate_corpus()
    
    # Step 2: Run benchmarks
    success = run_benchmarks()
    
    if not success:
        print("\n❌ Benchmarks failed. Check output above for errors.")
        return 1
    
    print("\n✅ Benchmarks completed successfully!")
    print("\n" + "="*70)
    print("Results have been printed above.")
    print("To export results to CSV/LaTeX, parse the test output or use pytest hooks.")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
