# Comprehensive RAG Example for PEaC

This example demonstrates all major features of PEaC (Prompt Engineering as Code) including **RAG (Retrieval-Augmented Generation)** capabilities.

## 📁 Directory Structure

```
comprehensive-example/
├── README.md                          # This file
├── comprehensive-analysis.yaml        # Main PEaC configuration
├── docs/                             # Documentation for RAG context
│   ├── python-architecture-patterns.md
│   ├── cli-design-guidelines.md
│   └── yaml-configuration-practices.md
├── code-examples/                    # Code examples for RAG
│   ├── config_parser.py
│   └── prompt_engineering.py
└── output-examples/                  # Example outputs for RAG
    ├── technical-analysis-example.md
    └── code-review-example.md
```

## 🎯 What This Example Demonstrates

### 1. **Local File Context**
- Single files with regex filtering
- Recursive directory scanning
- Extension-based file filtering
- Multiple file types (Python, YAML, Markdown)

### 2. **RAG (Retrieval-Augmented Generation)**
- FAISS vector database integration
- Semantic search across documentation
- Chunk-based retrieval with configurable sizes
- Overlap settings for better context
- Top-k results for relevance

### 3. **Multi-Source Context**
The example combines:
- **Instruction**: Defines AI behavior and role
- **Context**: Provides background information
  - Base context (project overview)
  - Local files (code and configs)
  - RAG search (semantic retrieval from docs)
- **Output**: Guides response format and style
  - Templates for structure
  - Examples for reference
  - RAG-based output examples
- **Query**: The final question/task

## 🚀 Quick Start

### Prerequisites

1. **Install PEaC dependencies:**
   ```bash
   cd /Users/gx1/Git/Unina/peac
   poetry install
   ```

2. **Install RAG dependencies (optional):**
   ```bash
   poetry add faiss-cpu sentence-transformers
   # Or for GPU support:
   # poetry add faiss-gpu sentence-transformers
   ```

### Option 1: Without RAG (Immediate Use)

The example works without RAG by using the local file context:

```bash
poetry run peac gui examples/comprehensive-analysis.yaml
```

This will:
- Load all local files specified in the YAML
- Skip RAG sections (FAISS files don't exist yet)
- Generate a comprehensive prompt from available context

### Option 2: With RAG (Full Features)

To enable RAG functionality, you need to create FAISS vector databases:

#### Step 1: Create FAISS Databases

You can use PEaC's built-in RAG indexing (if available) or create them manually:

```python
# create_faiss_indexes.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pathlib import Path

def create_faiss_index(source_folder: str, output_file: str):
    """Create FAISS index from documents in folder."""
    
    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Read all documents
    texts = []
    for file_path in Path(source_folder).rglob('*.md'):
        with open(file_path, 'r', encoding='utf-8') as f:
            texts.append(f.read())
    
    # Also read Python files
    for file_path in Path(source_folder).rglob('*.py'):
        with open(file_path, 'r', encoding='utf-8') as f:
            texts.append(f.read())
    
    # Create embeddings
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Save
    faiss.write_index(index, output_file)
    print(f"Created FAISS index: {output_file}")

# Create indexes
create_faiss_index(
    'examples/comprehensive-example/docs/',
    'examples/comprehensive-example/python_patterns.faiss'
)

create_faiss_index(
    'examples/comprehensive-example/code-examples/',
    'examples/comprehensive-example/codebase_examples.faiss'
)

create_faiss_index(
    'examples/comprehensive-example/output-examples/',
    'examples/comprehensive-example/analysis_examples.faiss'
)
```

Run the script:
```bash
python create_faiss_indexes.py
```

#### Step 2: Run with RAG

```bash
poetry run peac gui examples/comprehensive-analysis.yaml
```

Now all RAG sections will be active and semantic search will retrieve relevant context!

## 📝 Configuration Breakdown

### Instruction Section
```yaml
instruction:
  base:
    - "You are an expert Python software architect..."
    - "Analyze the provided code and documentation..."
```
Defines the AI's role and expertise.

### Context Section

#### Base Context
```yaml
context:
  base:
    - "This analysis is for the PEaC project."
    - "The project is a Python CLI tool..."
```
Provides project background.

#### Local Files
```yaml
local:
  main-module:
    preamble: "Main entry point of the application"
    source: "peac/main.py"
    filter: "def|class|import"
```
Includes actual project files with optional regex filtering.

#### RAG Context
```yaml
rag:
  python-knowledge:
    preamble: "Python architectural patterns from knowledge base"
    faiss_file: "examples/comprehensive-example/python_patterns.faiss"
    source_folder: "examples/comprehensive-example/docs/"
    query: "python architecture patterns cli design"
    top_k: 5
    chunk_size: 512
    overlap: 50
```
Performs semantic search to find most relevant chunks.

### Output Section

Guides the format and style of the response:
```yaml
output:
  base:
    - "Structure your response with clear sections..."
    - "Use markdown formatting..."
```

Plus references to templates and examples (local files and RAG).

### Query Section

The final task:
```yaml
query: |
  Based on the provided context, provide a comprehensive technical analysis covering:
  1. Architecture Overview
  2. Key Components
  3. Design Patterns
  ...
```

## 🔧 Customization

### Adjust RAG Parameters

```yaml
rag:
  your-search:
    query: "your search terms here"
    top_k: 3              # Number of results (1-10)
    chunk_size: 512       # Size of text chunks (128-2048)
    overlap: 50           # Overlap between chunks (0-200)
    filter: "pattern"     # Regex filter for results
```

**Guidelines:**
- **top_k**: Start with 3-5, increase if not enough context
- **chunk_size**: 
  - Small (256): For specific facts
  - Medium (512): Balanced (recommended)
  - Large (1024): For broader context
- **overlap**: 10-20% of chunk_size prevents losing context at boundaries

### Add More Sources

#### Add Local Files
```yaml
local:
  your-files:
    preamble: "Description"
    source: "path/to/file/or/directory"
    recursive: true        # For directories
    extension: "py"        # Filter by extension
    filter: "regex"        # Filter content
```

#### Add Web Sources (if supported)
```yaml
web:
  your-web-source:
    preamble: "Description"
    source: "https://example.com"
    xpath: "//div[@class='content']//p"
```

#### Add More RAG Searches
```yaml
rag:
  another-search:
    preamble: "What this searches for"
    faiss_file: "path/to/index.faiss"
    source_folder: "path/to/docs/"
    query: "your search query"
    top_k: 3
```

## 💡 Usage Tips

### 1. **Start Simple**
Begin with just local files, add RAG later when you need semantic search.

### 2. **Use Filters Wisely**
Regex filters reduce noise:
```yaml
filter: "class|def|import"  # Only class/function definitions
filter: "##|###"            # Only markdown headers
filter: "TODO|FIXME"        # Only comments with TODO/FIXME
```

### 3. **Optimize RAG Queries**
Good queries are specific:
- ❌ "code" (too broad)
- ✅ "python error handling best practices"
- ✅ "async/await implementation patterns"

### 4. **Layer Your Context**
Order matters:
1. Instructions (what role to play)
2. Base context (project overview)
3. Specific context (relevant files/searches)
4. Output guidelines (how to respond)
5. Query (what to do)

### 5. **Monitor Token Usage**
- Each section adds to token count
- Use filters to reduce content
- Prioritize most relevant sources
- Consider chunk_size vs. top_k tradeoff

## 📊 Expected Output

Running this example will generate a prompt containing:

1. **System instructions** - Role definition
2. **Project context** - PEaC overview
3. **Code analysis** - Main modules and core components
4. **Best practices** - From RAG-searched documentation
5. **Example patterns** - From code examples
6. **Output templates** - From example analyses
7. **Specific query** - The analysis task

This comprehensive context enables the LLM to provide detailed, informed analysis.

## 🐛 Troubleshooting

### "FAISS file not found"
**Solution:** Either:
- Run without RAG (local files still work)
- Create FAISS indexes (see Step 1 above)
- Comment out RAG sections in YAML

### "No results from RAG search"
**Possible causes:**
- Query doesn't match content well
- chunk_size too large/small
- filter is too restrictive

**Solutions:**
- Adjust query to be more specific
- Try different chunk_size values
- Remove or relax filter

### "Out of memory"
**Possible causes:**
- Too many large files
- chunk_size too large
- top_k too high

**Solutions:**
- Add filters to reduce content
- Decrease chunk_size
- Lower top_k value
- Process in smaller batches
