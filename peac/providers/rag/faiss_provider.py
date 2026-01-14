"""FAISS RAG provider - efficient vector search at scale"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import re
import pickle

from .base import BaseRAGProvider


class FaissProvider(BaseRAGProvider):
    """RAG provider using FAISS for scalable vector search"""
    
    DEFAULT_MODEL = 'BAAI/bge-small-en-v1.5'
    
    def __init__(self):
        super().__init__()
        self.model = None
        self.index = None
        self.metadata = None
        self._current_model_name = None
    
    def _initialize_model(self, model_name: str = DEFAULT_MODEL):
        """Initialize FastEmbed model for embedding generation"""
        try:
            from fastembed import TextEmbedding
            
            if self.model is None or self._current_model_name != model_name:
                print(f"Loading FastEmbed model: {model_name}")
                self.model = TextEmbedding(model_name=model_name)
                self._current_model_name = model_name
                print(f"Model loaded successfully")
            return self.model
        except ImportError:
            raise ImportError("fastembed library not installed. Install with: pip install fastembed")
    
    def parse(self, index_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Parse RAG request and return relevant documents using FAISS
        
        Args:
            index_path: Path to the FAISS index directory
            options: Dictionary containing:
                - query: Search query for RAG retrieval
                - source_folder: Folder/file to embed if index doesn't exist
                - top_k: Number of top results to return (default: 5)
                - chunk_size: Size of text chunks for embedding (default: 512)
                - overlap: Overlap between chunks (default: 50)
                - force_override: Force recreation of index (default: False)
                - embedding_model: Model name for embedding (default: BAAI/bge-small-en-v1.5)
                - provider_config: Provider-specific options:
                    - index_type: 'flat', 'ivf', 'hnsw' (default: 'flat')
                    - metric_type: 'L2', 'IP' (default: 'L2')
                    - n_clusters: Number of clusters for IVF (default: 100)
        
        Returns:
            Retrieved and ranked text content
        """
        if options is None:
            options = {}
        
        query = options.get('query', '')
        if not query:
            return "Error: No query provided for RAG search"
        
        source_folder = options.get('source_folder', '')
        top_k = options.get('top_k', 5)
        chunk_size = options.get('chunk_size', 512)
        overlap = options.get('overlap', 50)
        force_override = options.get('force_override', False)
        embedding_model = options.get('embedding_model', self.DEFAULT_MODEL)
        provider_config = options.get('provider_config', {})
        
        self.index_type = provider_config.get('index_type', 'flat')
        self.metric_type = provider_config.get('metric_type', 'L2')
        self.n_clusters = provider_config.get('n_clusters', 100)
        
        # Check if index exists and if we should override it
        should_create_index = force_override or not self._index_exists(index_path)
        
        if should_create_index:
            if source_folder:
                print(f"[RAG DEBUG] source_folder value: {source_folder}")
                print(f"[RAG DEBUG] source_folder exists: {os.path.exists(source_folder)}")
                if force_override:
                    print(f"Force override enabled. Recreating index from: {source_folder}")
                else:
                    print(f"Index not found. Creating from source: {source_folder}")
                
                success = self._create_index(index_path, source_folder, chunk_size, overlap, embedding_model)
                if not success:
                    return f"Error: Failed to create index from {source_folder}"
            else:
                print(f"Index not found and no source folder provided. Creating empty default index...")
                success = self._create_default_index(index_path, embedding_model)
                if not success:
                    return f"Error: Failed to create default index at {index_path}"
        
        # Load index and perform search
        try:
            results = self._search_index(index_path, query, top_k, embedding_model)
            return self._format_results(results, query)
        except Exception as e:
            return f"Error during RAG search: {str(e)}"
    
    def _index_exists(self, index_path: str) -> bool:
        """Check if FAISS index exists at the given path"""
        index_dir = Path(index_path)
        return (index_dir.is_dir() and 
                (index_dir / 'index.faiss').exists() and 
                (index_dir / 'metadata.pkl').exists())
    
    def _create_default_index(self, index_path: str, embedding_model: str = DEFAULT_MODEL) -> bool:
        """Create a default empty index with sample data"""
        try:
            model = self._initialize_model(embedding_model)
            
            sample_chunks = [
                "This is a default empty index. Add content by specifying a source folder or updating the index directly.",
                "FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering.",
                "Vector search enables semantic similarity matching across documents and texts.",
                "The RAG system can work with any text files, PDFs, DOCX documents, and more.",
                "FAISS supports multiple index types for different scale and accuracy trade-offs.",
            ]
            
            chunk_metadata = [
                {'source': 'default', 'chunk_id': i, 'text': chunk}
                for i, chunk in enumerate(sample_chunks)
            ]
            
            print(f"Creating default FAISS index with {len(sample_chunks)} sample chunks...")
            
            # Generate embeddings
            embeddings_list = list(model.embed(sample_chunks, batch_size=256))
            embeddings_array = self._convert_embeddings(embeddings_list)
            
            # Create FAISS index
            index = self._create_faiss_index(embeddings_array)
            
            # Save index
            index_dir = Path(index_path)
            index_dir.mkdir(parents=True, exist_ok=True)
            
            import faiss
            faiss.write_index(index, str(index_dir / 'index.faiss'))
            
            metadata = {
                'provider': 'faiss',
                'embedding_model': embedding_model,
                'index_type': self.index_type,
                'metric_type': self.metric_type,
                'chunks': chunk_metadata,
            }
            
            with open(index_dir / 'metadata.pkl', 'wb') as f:
                pickle.dump(metadata, f)
            
            print(f"Default FAISS index created successfully: {index_path}")
            print(f"Total sample chunks: {len(sample_chunks)}")
            print(f"Index type: {self.index_type}, Metric: {self.metric_type}")
            return True
            
        except ImportError:
            print("FAISS not installed. Install with: pip install faiss-cpu or pip install faiss-gpu")
            return False
        except Exception as e:
            print(f"Error creating default FAISS index: {str(e)}")
            return False
    
    def _create_index(self, index_path: str, source_folder: str, chunk_size: int = 512, 
                     overlap: int = 50, embedding_model: str = DEFAULT_MODEL) -> bool:
        """Create FAISS index from source folder/file"""
        try:
            model = self._initialize_model(embedding_model)
            
            documents = self._collect_documents(source_folder)
            if not documents:
                print(f"No documents found in {source_folder}")
                return False
            
            print(f"Found {len(documents)} documents. Creating chunks...")
            
            chunks = []
            chunk_metadata = []
            
            for doc_path, content in documents:
                doc_chunks = self._create_chunks(content, chunk_size, overlap)
                for i, chunk in enumerate(doc_chunks):
                    chunks.append(chunk)
                    chunk_metadata.append({
                        'source': doc_path,
                        'chunk_id': i,
                        'text': chunk
                    })
            
            print(f"Created {len(chunks)} chunks. Generating embeddings...")
            
            embeddings_list = list(model.embed(chunks, batch_size=256))
            embeddings_array = self._convert_embeddings(embeddings_list)
            
            print(f"Creating FAISS index with {len(chunks)} vectors...")
            
            # Create FAISS index
            index = self._create_faiss_index(embeddings_array)
            
            # Save index
            index_dir = Path(index_path)
            index_dir.mkdir(parents=True, exist_ok=True)
            
            import faiss
            faiss.write_index(index, str(index_dir / 'index.faiss'))
            
            metadata = {
                'provider': 'faiss',
                'embedding_model': embedding_model,
                'index_type': self.index_type,
                'metric_type': self.metric_type,
                'chunks': chunk_metadata,
            }
            
            with open(index_dir / 'metadata.pkl', 'wb') as f:
                pickle.dump(metadata, f)
            
            print(f"FAISS index created successfully: {index_path}")
            print(f"Total chunks: {len(chunks)}")
            print(f"Index type: {self.index_type}, Metric: {self.metric_type}")
            return True
            
        except ImportError:
            print("FAISS not installed. Install with: pip install faiss-cpu or pip install faiss-gpu")
            return False
        except Exception as e:
            print(f"Error creating FAISS index: {str(e)}")
            return False
    
    def _create_faiss_index(self, embeddings_array):
        """Create appropriate FAISS index based on configuration"""
        try:
            import faiss
            import numpy as np
            
            d = embeddings_array.shape[1]  # Dimension
            
            if self.index_type == 'flat':
                if self.metric_type == 'IP':
                    index = faiss.IndexFlatIP(d)
                else:  # L2
                    index = faiss.IndexFlatL2(d)
            
            elif self.index_type == 'ivf':
                nlist = min(self.n_clusters, embeddings_array.shape[0] // 4)
                quantizer = faiss.IndexFlatL2(d) if self.metric_type == 'L2' else faiss.IndexFlatIP(d)
                index = faiss.IndexIVFFlat(quantizer, d, nlist)
                index.train(embeddings_array.astype(np.float32))
            
            elif self.index_type == 'hnsw':
                index = faiss.IndexHNSWFlat(d, 32)
                if self.metric_type == 'IP':
                    index.metric_type = faiss.METRIC_INNER_PRODUCT
            
            else:
                # Default to flat
                index = faiss.IndexFlatL2(d)
            
            index.add(embeddings_array.astype(np.float32))
            return index
            
        except ImportError:
            raise ImportError("FAISS not installed")
    
    def _collect_documents(self, source_path: str) -> List[tuple]:
        """Collect documents from source path"""
        documents = []
        source_path = Path(source_path)
        
        if source_path.is_file():
            content = self._read_file_content(str(source_path))
            if content:
                documents.append((str(source_path), content))
        elif source_path.is_dir():
            for file_path in source_path.rglob('*'):
                if file_path.is_file() and self._is_text_file(file_path):
                    content = self._read_file_content(str(file_path))
                    if content:
                        documents.append((str(file_path), content))
        
        return documents
    
    @staticmethod
    def _is_text_file(file_path: Path) -> bool:
        """Check if file is a supported text file"""
        text_extensions = {'.txt', '.md', '.py', '.js', '.java', '.cpp', '.c', '.h', 
                          '.html', '.css', '.xml', '.json', '.yaml', '.yml', '.rst',
                          '.pdf', '.docx', '.doc'}
        return file_path.suffix.lower() in text_extensions
    
    def _read_file_content(self, file_path: str) -> str:
        """Read content from various file types"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.pdf':
                return self._read_pdf(file_path)
            elif file_ext in ['.docx', '.doc']:
                return self._read_docx(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                return self._clean_text(content)
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            return ""
    
    @staticmethod
    def _read_pdf(file_path: str) -> str:
        """Read PDF content using pdfplumber"""
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return FaissProvider._clean_text(text)
        except ImportError:
            print("pdfplumber not available for PDF reading")
            return ""
        except Exception as e:
            print(f"Error reading PDF {file_path}: {str(e)}")
            return ""
    
    @staticmethod
    def _read_docx(file_path: str) -> str:
        """Read DOCX content"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return FaissProvider._clean_text(text)
        except ImportError:
            print("python-docx not available for DOCX reading")
            return ""
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {str(e)}")
            return ""
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize extracted text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
        text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
        text = re.sub(r'(\w)\n(\w)', r'\1 \2', text)
        text = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', text)
        text = re.sub(r'(\w)([A-Z]+)(\w)', r'\1 \2 \3', text)
        text = ' '.join(text.split())
        
        return text
    
    @staticmethod
    def _create_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
        """Create overlapping text chunks"""
        text = FaissProvider._clean_text(text)
        
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            if end < len(text):
                sentence_end = max(
                    chunk.rfind('. '),
                    chunk.rfind('! '),
                    chunk.rfind('? ')
                )
                
                if sentence_end < chunk_size * 0.6:
                    sentence_end = chunk.rfind('\n\n')
                
                if sentence_end < chunk_size * 0.6:
                    sentence_end = chunk.rfind(' ')
                
                if sentence_end > chunk_size * 0.4:
                    chunk = chunk[:sentence_end + 1]
                    end = start + sentence_end + 1
            
            chunk = chunk.strip()
            if len(chunk) > 50:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def _search_index(self, index_path: str, query: str, top_k: int, 
                     embedding_model: str = DEFAULT_MODEL) -> List[Dict]:
        """Search FAISS index for relevant documents"""
        try:
            import faiss
            import numpy as np
            
            model = self._initialize_model(embedding_model)
            
            # Load index and metadata
            index_dir = Path(index_path)
            index = faiss.read_index(str(index_dir / 'index.faiss'))
            
            with open(index_dir / 'metadata.pkl', 'rb') as f:
                metadata = pickle.load(f)
            
            chunks_metadata = metadata['chunks']
            
            # Generate query embedding
            query_embedding_raw = list(model.embed([query]))[0]
            query_embedding = query_embedding_raw.tolist() if hasattr(query_embedding_raw, 'tolist') else query_embedding_raw
            query_array = np.array([query_embedding], dtype=np.float32)
            
            # Search
            distances, indices = index.search(query_array, min(top_k, len(chunks_metadata)))
            
            # Prepare results
            results = []
            for rank, idx in enumerate(indices[0], 1):
                if idx < len(chunks_metadata):
                    result = chunks_metadata[int(idx)].copy()
                    # Convert distance to similarity (for L2 distance, use negative distance)
                    score = 1.0 / (1.0 + distances[0][rank - 1]) if distances[0][rank - 1] > 0 else 0.0
                    result['score'] = float(score)
                    result['rank'] = rank
                    results.append(result)
            
            return results
            
        except ImportError:
            print("FAISS not installed")
            return []
        except Exception as e:
            print(f"Error searching FAISS index: {str(e)}")
            return []
    
    @staticmethod
    def _convert_embeddings(embeddings_list):
        """Convert embedding list to numpy array"""
        try:
            import numpy as np
            return np.array([
                emb.tolist() if hasattr(emb, 'tolist') else emb 
                for emb in embeddings_list
            ], dtype=np.float32)
        except Exception as e:
            print(f"Error converting embeddings: {str(e)}")
            raise
    
    def _format_results(self, results: List[Dict], query: str) -> str:
        """Format search results for output"""
        if not results:
            return f"No relevant documents found for query: '{query}'"
        
        output = f"RAG Search Results (FAISS) for: '{query}'\n"
        output += "=" * 50 + "\n\n"
        
        for result in results:
            output += f"Rank {result['rank']} (Score: {result['score']:.3f})\n"
            output += f"Source: {result['source']}\n"
            output += f"Chunk ID: {result['chunk_id']}\n"
            output += "-" * 30 + "\n"
            
            text = result['text']
            text = self._clean_display_text(text)
            
            if len(text) > 500:
                truncated = text[:500]
                last_sentence = max(
                    truncated.rfind('. '),
                    truncated.rfind('! '),
                    truncated.rfind('? ')
                )
                if last_sentence > 300:
                    text = truncated[:last_sentence + 1]
                else:
                    text = truncated + "..."
            
            output += text + "\n"
            output += "=" * 50 + "\n\n"
        
        return output
    
    @staticmethod
    def _clean_display_text(text: str) -> str:
        """Additional cleaning for display purposes"""
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        text = re.sub(r'(\w)([.!?])([A-Z])', r'\1\2 \3', text)
        text = re.sub(r'([a-z])([A-Z][a-z]+)', r'\1 \2', text)
        text = re.sub(r'([a-z])([A-Z][a-z]+)([a-z])([A-Z])', r'\1 \2 \3 \4', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def apply_filter(self, text: str, filter_regex: str) -> str:
        """Apply regex filter to retrieved text"""
        if not filter_regex:
            return text
            
        try:
            pattern = re.compile(filter_regex, re.MULTILINE)
            lines = text.split('\n')
            filtered_lines = [line for line in lines if pattern.search(line)]
            return '\n'.join(filtered_lines)
        except re.error:
            return text
