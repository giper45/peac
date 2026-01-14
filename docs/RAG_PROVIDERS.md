# RAG Providers: FastEmbed vs FAISS

PEaC ora supporta **due provider RAG** per il vector search: **FastEmbed** (leggero, predefinito per GUI) e **FAISS** (scalabile, per dataset grandi).

## Quick Comparison

| Caratteristica | FastEmbed | FAISS |
|---|---|---|
| **Setup** | Immediato, no dipendenze C++ | Richiede `faiss-cpu` o `faiss-gpu` |
| **Peso** | ~100MB | ~200-500MB |
| **Velocità embedding** | Rapida, CPU ottimizzata | Molto rapida, GPU supportato |
| **Ricerca** | Brute force (ottimale fino a ~100k docs) | Scalabile (milioni di docs) |
| **Index tipo** | JSON file | Directory FAISS + pickle metadata |
| **Usare quando** | Prototipi, dataset piccoli-medi | Production, dataset grandi |

## Configuration in YAML

### Default (FastEmbed)

Se non specificate `provider`, viene usato **FastEmbed**:

```yaml
rag:
  search_python:
    index_path: "indexes/python.json"
    source_folder: "docs/python"
    query: "Come funziona questo?"
    top_k: 5
```

### Explicit FastEmbed

```yaml
rag:
  search_with_config:
    provider: "fastembed"
    index_path: "indexes/docs.json"
    source_folder: "docs"
    query: "What's this?"
    embedding_model: "BAAI/bge-small-en-v1.5"
    provider_config:
      batch_size: 256
      device: "cpu"  # or "gpu"
    top_k: 5
    chunk_size: 512
    overlap: 50
```

### FAISS (Scalable)

```yaml
rag:
  large_dataset:
    provider: "faiss"
    index_path: "indexes/large_dataset"  # Directory, not file
    source_folder: "data/large"
    query: "Find relevant documents"
    embedding_model: "BAAI/bge-small-en-v1.5"
    provider_config:
      index_type: "ivf"          # 'flat', 'ivf', 'hnsw'
      metric_type: "L2"          # 'L2' or 'IP'
      n_clusters: 100            # Only for 'ivf'
    top_k: 10
    chunk_size: 512
    overlap: 50
```

## Provider Configuration Details

### FastEmbed Provider Config

```yaml
provider_config:
  batch_size: 256    # Batch size per embedding (default: 256)
  device: "cpu"      # "cpu" or "gpu" (default: cpu)
```

### FAISS Provider Config

```yaml
provider_config:
  index_type: "flat"     # Options:
                         #   - "flat": Simple Euclidean (<=100k docs)
                         #   - "ivf": Inverted file (100k-10M docs)
                         #   - "hnsw": Hierarchical NSW (realtime)
  metric_type: "L2"      # Options:
                         #   - "L2": Euclidean distance (default)
                         #   - "IP": Inner product (cosine similarity)
  n_clusters: 100        # Only for "ivf" type
                         # Rule of thumb: sqrt(N_docs) / 10
```

## CLI Usage

### Using FastEmbed (default)

```bash
poetry run peac gui
```

The GUI uses **FastEmbed by default** for all RAG operations (recommended for Windows users).

### Using FAISS from CLI

```bash
poetry run peac your_config.yaml
```

Where your YAML has:

```yaml
rag:
  search:
    provider: "faiss"
    index_path: "indexes/my_index"
    source_folder: "data"
    query: "your query"
```

## Installation

### FastEmbed (included)

```bash
# FastEmbed is lightweight and installed by default
pip install fastembed
```

### FAISS (optional)

```bash
# CPU version
pip install faiss-cpu

# GPU version (requires CUDA)
pip install faiss-gpu
```

## Migration from `faiss_file` to `index_path`

**Old format** (still supported for backward compatibility):

```yaml
rag:
  my_rule:
    faiss_file: "index.json"
    query: "..."
```

**New format** (recommended):

```yaml
rag:
  my_rule:
    index_path: "index.json"  # or "indexes/my_index" for FAISS
    provider: "fastembed"      # explicit
    query: "..."
```

## Examples

See [rag-dual-provider.yaml](./rag-dual-provider.yaml) for complete examples con both providers.

## Best Practices

1. **For GUI (Windows/Mac/Linux)**: Use **FastEmbed** (default)
   - No additional dependencies
   - Fast enough for most use cases
   - Lower memory footprint

2. **For CLI with large datasets**: Use **FAISS**
   - Better performance at scale
   - Multiple index strategies available
   - Can handle millions of documents

3. **Embedding models**: All providers support the same models:
   - `BAAI/bge-small-en-v1.5` (256 dim, fast)
   - `BAAI/bge-base-en-v1.5` (768 dim, better quality)
   - And many others from HuggingFace

4. **Index paths**:
   - **FastEmbed**: Use `.json` file extension
   - **FAISS**: Use directory path (no extension)

## Troubleshooting

### "RAG provider not available"

Install the missing provider:

```bash
pip install fastembed      # For FastEmbed
pip install faiss-cpu      # For FAISS
```

### "Invalid index structure"

Recreate the index:

```yaml
rag:
  my_rule:
    index_path: "..."
    source_folder: "..."
    force_override: true   # Will recreate
    query: "..."
```

### FAISS performance is slow

Adjust `index_type` and `n_clusters`:

```yaml
provider_config:
  index_type: "hnsw"     # Faster for realtime
  # or
  index_type: "ivf"
  n_clusters: 50         # Fewer clusters = faster but less accurate
```

### Different embedding models

Both providers support any FastEmbed model. To use a different model:

```yaml
rag:
  my_rule:
    embedding_model: "BAAI/bge-base-en-v1.5"  # Better quality
    ...
```

Note: Switching embedding models requires index recreation.
