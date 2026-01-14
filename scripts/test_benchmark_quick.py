#!/usr/bin/env python3
"""
Quick benchmark test with reduced runs to verify setup.

Usage:
  poetry run python scripts/test_benchmark_quick.py           # FastEmbed only
  poetry run python scripts/test_benchmark_quick.py --faiss   # FAISS only
  poetry run python scripts/test_benchmark_quick.py --both    # Both providers
"""
import sys

# Temporarily modify NUM_RUNS for quick testing
import tests.test_performance as tp
tp.NUM_RUNS = 5  # Reduce from 50 to 5 for quick test

def main(argv=None):
    argv = argv or sys.argv[1:]
    run_fastembed = True
    run_faiss = False
    if "--faiss" in argv:
        run_fastembed = False
        run_faiss = True
    if "--both" in argv:
        run_fastembed = True
        run_faiss = True

    tests_to_run = []
    if run_fastembed:
        tests_to_run.append("tests/test_performance.py::TestRAGPerformance::test_fastembed_performance")
    if run_faiss:
        tests_to_run.append("tests/test_performance.py::TestRAGPerformance::test_faiss_performance")

    if not tests_to_run:
        tests_to_run.append("tests/test_performance.py::TestRAGPerformance::test_fastembed_performance")

    import pytest
    return pytest.main(tests_to_run + ["-v", "-s"])

if __name__ == "__main__":
    sys.exit(main())
