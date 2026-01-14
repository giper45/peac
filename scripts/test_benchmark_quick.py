#!/usr/bin/env python3
"""
Quick benchmark test with reduced runs to verify setup
"""
import sys
import os

# Temporarily modify NUM_RUNS for quick testing
import tests.test_performance as tp
tp.NUM_RUNS = 5  # Reduce from 50 to 5 for quick test

# Run pytest
import pytest
sys.exit(pytest.main([
    "tests/test_performance.py::TestRAGPerformance::test_fastembed_performance",
    "-v", "-s"
]))
