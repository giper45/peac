# RAG Examples for PEaC

This directory contains examples demonstrating RAG (Retrieval-Augmented Generation) capabilities with different providers.

## Available Examples

### 1. **rag-simple.yaml** - Quick Start
Minimal configuration for getting started with RAG.
- Uses FastEmbed (default provider)
- Automatic index creation
- Searches sample-docs/ folder

```bash
poetry run peac prompt examples/rag-simple.yaml
```

### 2. **rag-sample-docs.yaml** - Complete Example
Full-featured example with sample documentation.
- Demonstrates semantic search across multiple file types
- Includes comprehensive comments
- Sample queries provided

```bash
poetry run peac prompt examples/rag-sample-docs.yaml
```

### 3. **rag-fastembed.yaml** - FastEmbed Provider
Detailed FastEmbed configuration with all options.
- Lightweight, JSON-based storage
- Best for: Small-medium datasets, prototyping, Windows
- Portable indexes, no C++ compilation

```bash
poetry run peac prompt examples/rag-fastembed.yaml
```

### 4. **rag-faiss.yaml** - FAISS Provider
High-performance FAISS configuration.
- Scalable for large datasets
- Multiple index types (flat, ivf, hnsw)
- Best for: Production, large knowledge bases, CLI users

**Requirements:**
```bash
poetry add faiss-cpu  # or faiss-gpu
```

```bash
poetry run peac prompt examples/rag-faiss.yaml
```

## Provider Comparison

| Feature | FastEmbed | FAISS |
|---------|-----------|-------|
| **Storage** | JSON files | Binary indexes |
| **Setup** | No dependencies | Requires faiss-cpu/gpu |
| **Performance** | Fast (<50k docs) | Optimized (>100k docs) |
| **Index Types** | Simple | Multiple (flat/ivf/hnsw) |
| **Memory** | Lightweight | Can be heavy |
| **Portability** | Excellent | Platform-specific |
| **Best For** | Prototyping, GUI | Production, CLI |

## Sample Documentation

The `sample-docs/` folder contains example documents:
- **python_best_practices.md** - Python coding standards
- **api_design.md** - REST API guidelines
- **data_processor.py** - Python code example
- **database_design.txt** - Database design principles
- **architecture_patterns.md** - Software architecture patterns

## Configuration Guide

### Common Parameters

```yaml
rag:
  my_search:
    provider: "fastembed"  # or "faiss"
    index_path: "path/to/index"
    source_folder: "path/to/docs"
    query: "Your search query"
    top_k: 5              # Number of results
    chunk_size: 512       # Text chunk size
    overlap: 50           # Chunk overlap
    embedding_model: "BAAI/bge-small-en-v1.5"
```

### FastEmbed Specific

```yaml
provider_config:
  batch_size: 256  # Embeddings per batch
  device: "cpu"    # or "gpu"
```

### FAISS Specific

```yaml
provider_config:
  index_type: "flat"    # "flat", "ivf", or "hnsw"
  metric_type: "L2"     # "L2" or "IP"
  n_clusters: 100       # For IVF only
```

## Tips

1. **First Run**: Index is created automatically from `source_folder`
2. **Updating Index**: Delete index file to rebuild from source
3. **Multiple Searches**: Use different index names for different document sets
4. **Query Tuning**: Adjust `top_k` and `chunk_size` for better results
5. **Performance**: Use FAISS for datasets >50k documents

## Troubleshooting

### FastEmbed not installed
```bash
poetry add fastembed
```

### FAISS not installed
```bash
poetry add faiss-cpu  # CPU version
poetry add faiss-gpu  # GPU version (requires CUDA)
```

### Index creation fails
- Check that `source_folder` path is correct (relative to YAML file)
- Ensure folder contains supported files (.txt, .md, .py, .pdf, .docx)
- Check file permissions

### Poor search results
- Increase `top_k` for more results
- Adjust `chunk_size` (larger for technical docs, smaller for code)
- Try different `embedding_model` options
- Improve document quality and formatting
