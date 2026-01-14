# PEaC Reproducibility Package

This directory contains the reproducibility infrastructure for the PEaC framework, enabling validation of functional correctness and performance benchmarks presented in our research paper.

## Overview

The reproducibility package includes:

1. **Functional Test Suite** (`tests/test_peac_core.py`, `tests/test_rag.py`)
   - 114 automated tests validating YAML parsing, EBNF grammar compliance, and provider functionality
   - Tests all 24 example YAML files from the paper

2. **Performance Benchmark Suite** (`tests/test_performance.py`)
   - FastEmbed vs FAISS provider comparison
   - Metrics: peak memory usage, query response time, index creation time, disk space
   - 50 runs per provider for statistical reliability

3. **Docker Container** (`Dockerfile`, `docker-compose.yml`)
   - Isolated reproducible environment
   - No manual dependency installation required

## Quick Start

### Option 1: Using Docker (Recommended)

```bash
# Build container
docker-compose build

# Run functional tests
docker-compose run peac-tests

# Run performance benchmarks
docker-compose run peac-benchmarks
```

### Option 2: Local Execution

```bash
# Install dependencies
poetry install

# Run functional tests (114 tests)
make test

# Run performance benchmarks (50 runs, ~10 minutes)
poetry run python scripts/run_benchmarks.py
```

## Performance Benchmarks

### Test Configuration

- **Corpus**: 100 synthetic documents (avg. 10KB each)
- **Repetitions**: 50 runs per provider
- **Queries**: 10 semantic search queries per run
- **Providers**: FastEmbed (default), FAISS (optional)

### Running Benchmarks

```bash
# Generate synthetic corpus (if not exists)
poetry run python tests/utils/generate_synthetic_corpus.py tests/benchmark_corpus 100 10

# Run benchmarks
poetry run pytest tests/test_performance.py -v -s

# Compare providers
poetry run pytest tests/test_performance.py::TestRAGPerformance::test_compare_providers -v -s
```

### Expected Output

Benchmarks report:
- **Index Creation Time**: Time to build semantic search index
- **Query Response Time**: Average latency per query
- **Peak Memory Usage**: Maximum RAM consumption
- **Index Size**: Disk space required for index storage

Results validate FastEmbed's suitability for general-purpose hardware.

## System Requirements

### Minimum Specifications

- **CPU**: 2 cores (4 recommended)
- **RAM**: 4GB (8GB recommended)
- **Disk**: 2GB free space
- **OS**: Linux, macOS, or Windows with Docker

### Software Dependencies

- Python 3.11+
- Poetry 1.8+
- Docker (for containerized execution)

## Test Suite Structure

```
tests/
├── test_peac_core.py          # 89 functional tests (YAML parsing, EBNF compliance)
├── test_rag.py                # 22 RAG provider tests
├── test_performance.py        # Performance benchmarks (NEW)
├── test_path_resolver.py      # 4 path resolution tests
└── utils/
    └── generate_synthetic_corpus.py  # Corpus generator
```

## Reproducing Paper Results

### Functional Validation (Table 1 in paper)

```bash
# Run all functional tests
poetry run pytest tests/ -v

# Expected: 114 passed, 1 skipped
```

### Performance Comparison (Appendix A in paper)

```bash
# Run benchmarks with results export
poetry run python scripts/run_benchmarks.py

# Results are printed to console
# To include in paper, copy values to LaTeX table
```

### Token Reduction Metrics (Section 6.4 in paper)

The token reduction experiment (24.07% reduction) is validated through:

```bash
# Test modular inheritance mechanism
poetry run pytest tests/test_peac_core.py::TestYAMLParsing -v

# All 24 YAML examples should parse correctly
```

## Troubleshooting

### Issue: FAISS not installed

FAISS is optional. To install:

```bash
# macOS/Linux
make install-faiss

# Or manually
poetry run pip install faiss-cpu
```

### Issue: Out of memory during benchmarks

Reduce corpus size or number of runs:

```python
# Edit tests/test_performance.py
CORPUS_SIZE = 50  # Reduce from 100
NUM_RUNS = 25     # Reduce from 50
```

### Issue: Slow benchmark execution

Expected runtime: ~10 minutes for 50 runs. To speed up:

```bash
# Run with fewer repetitions (less statistical reliability)
poetry run pytest tests/test_performance.py -v -s
# Then edit NUM_RUNS = 10 in test_performance.py
```

## Citation

If you use this reproducibility package, please cite:

```bibtex
@article{peac2026,
  title={Advancing Prompt Engineering as Code (PEaC): Formal Specifications, External Data Integration, and Graphical Interface},
  author={[Your Names]},
  journal={[Journal Name]},
  year={2026}
}
```

## Hardware Specifications

Benchmark results in the paper were obtained on:
- **CPU**: [INSERT YOUR CPU]
- **RAM**: [INSERT YOUR RAM]
- **OS**: [INSERT YOUR OS]
- **Python**: 3.11.2
- **Poetry**: 1.8.0

Please report your hardware specifications when sharing benchmark results to enable meaningful comparisons.

## Contact

For issues or questions about reproducibility:
- GitHub Issues: [https://github.com/giper45/peac/issues](https://github.com/giper45/peac/issues)
- Email: [INSERT YOUR EMAIL]

## License

This reproducibility package is licensed under the same license as PEaC (see LICENSE.txt).
