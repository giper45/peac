"""FastEmbed RAG provider - lightweight embeddings without PyTorch"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import re

from .base import BaseRAGProvider


class FastembedProvider(BaseRAGProvider):
    """RAG provider using FastEmbed for lightweight embeddings"""
    
    DEFAULT_MODEL = 'BAAI/bge-small-en-v1.5'
    
    def __init__(self):
        super().__init__()
        self.model = None
        self.embeddings_cache = {}
        self._current_model_name = None
    
    def _initialize_model(self, model_name: str = DEFAULT_MODEL):
        """Initialize FastEmbed model (lightweight, no PyTorch dependency)"""
        try:
            from fastembed import TextEmbedding
            
            # Reload model only if model_name is different or model is None
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
        Parse RAG request and return relevant documents using FastEmbed
        
        Args:
            index_path: Path to the vector index file (JSON format)
            options: Dictionary containing:
                - query: Search query for RAG retrieval
                - source_folder: Folder/file to embed if index file doesn't exist
                - top_k: Number of top results to return (default: 5)
                - chunk_size: Size of text chunks for embedding (default: 512)
                - overlap: Overlap between chunks (default: 50)
                - force_override: Force recreation of index (default: False)
                - embedding_model: Model name for embedding (default: BAAI/bge-small-en-v1.5)
                - provider_config: Provider-specific options:
                    - batch_size: Batch size for embedding (default: 256)
                    - device: 'cpu' or 'gpu' (default: 'cpu')
        
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
        
        self.batch_size = provider_config.get('batch_size', 256)
        self.device = provider_config.get('device', 'cpu')
        
        # Check if index file exists and if we should override it
        should_create_index = force_override or not os.path.exists(index_path)
        
        if should_create_index:
            # If source_folder is provided, ALWAYS create index from source folder documents
            if source_folder:
                print(f"[RAG DEBUG] source_folder value: {source_folder}")
                print(f"[RAG DEBUG] source_folder exists: {os.path.exists(source_folder)}")
                if force_override:
                    print(f"Force override enabled. Recreating index from: {source_folder}")
                else:
                    print(f"Index file '{index_path}' not found. Creating from source: {source_folder}")
                    
                success = self._create_index(index_path, source_folder, chunk_size, overlap, embedding_model)
                if not success:
                    return f"Error: Failed to create index from {source_folder}"
            else:
                # Only create default index if NO source folder is provided
                print(f"Index file '{index_path}' not found and no source folder provided. Creating empty default index...")
                success = self._create_default_index(index_path, embedding_model)
                if not success:
                    return f"Error: Failed to create default index at {index_path}"
        
        # Load index and perform search
        try:
            results = self._search_index(index_path, query, top_k, embedding_model)
            return self._format_results(results, query)
        except Exception as e:
            return f"Error during RAG search: {str(e)}"
    
    def _create_default_index(self, index_file: str, embedding_model: str = DEFAULT_MODEL) -> bool:
        """Create a default empty index with sample data"""
        try:
            model = self._initialize_model(embedding_model)
            
            # Create sample chunks with basic information
            sample_chunks = [
                "This is a default empty index. Add content by specifying a source folder or updating the index file directly.",
                "FastEmbed provides lightweight, efficient text embeddings without requiring PyTorch or heavy GPU dependencies.",
                "Vector search enables semantic similarity matching across documents and texts.",
                "The RAG system can work with any text files, PDFs, DOCX documents, and more.",
                "Customize the embedding model by selecting from available FastEmbed models.",
            ]
            
            chunk_metadata = [
                {'source': 'default', 'chunk_id': i, 'text': chunk}
                for i, chunk in enumerate(sample_chunks)
            ]
            
            print(f"Creating default index with {len(sample_chunks)} sample chunks...")
            
            # Generate embeddings for sample chunks
            embeddings_list = list(model.embed(sample_chunks, batch_size=self.batch_size))
            
            # Convert numpy arrays to lists for JSON serialization
            embeddings_list = [emb.tolist() if hasattr(emb, 'tolist') else emb for emb in embeddings_list]
            
            # Create index structure
            index_data = {
                'provider': 'fastembed',
                'embedding_model': embedding_model,
                'chunks': chunk_metadata,
                'embeddings': embeddings_list
            }
            
            # Save index to file
            index_dir = os.path.dirname(index_file)
            if index_dir:
                os.makedirs(index_dir, exist_ok=True)
            
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
            
            print(f"Default index created successfully: {index_file}")
            print(f"Total sample chunks: {len(sample_chunks)}")
            print(f"Used embedding model: {embedding_model}")
            return True
            
        except Exception as e:
            print(f"Error creating default index: {str(e)}")
            return False
    
    def _create_index(self, index_file: str, source_folder: str, chunk_size: int = 512, overlap: int = 50, embedding_model: str = DEFAULT_MODEL) -> bool:
        """Create vector index from source folder/file using FastEmbed"""
        try:
            model = self._initialize_model(embedding_model)
            
            # Collect all text documents
            documents = self._collect_documents(source_folder)
            if not documents:
                print(f"No documents found in {source_folder}")
                return False
            
            print(f"Found {len(documents)} documents. Creating chunks...")
            
            # Create text chunks
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
            
            print(f"Created {len(chunks)} chunks. Generating embeddings with FastEmbed...")
            
            # Generate embeddings using FastEmbed (very fast, no GPU needed)
            embeddings_list = list(model.embed(chunks, batch_size=self.batch_size))
            
            # Convert numpy arrays to lists for JSON serialization
            embeddings_list = [emb.tolist() if hasattr(emb, 'tolist') else emb for emb in embeddings_list]
            
            # Create index structure
            index_data = {
                'provider': 'fastembed',
                'embedding_model': embedding_model,
                'chunks': chunk_metadata,
                'embeddings': embeddings_list
            }
            
            # Save index to file
            index_dir = os.path.dirname(index_file)
            if index_dir:
                os.makedirs(index_dir, exist_ok=True)
            
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
            
            print(f"Index created successfully: {index_file}")
            print(f"Total chunks: {len(chunks)}")
            print(f"Used embedding model: {embedding_model}")
            return True
            
        except Exception as e:
            print(f"Error creating index: {str(e)}")
            return False
    
    def _collect_documents(self, source_path: str) -> List[tuple]:
        """Collect documents from source path"""
        documents = []
        source_path = Path(source_path)
        
        if source_path.is_file():
            content = self._read_file_content(str(source_path))
            if content:
                documents.append((str(source_path), content))
        elif source_path.is_dir():
            # Recursively collect all text files
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
                # Regular text file
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
            return FastembedProvider._clean_text(text)
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
            return FastembedProvider._clean_text(text)
        except ImportError:
            print("python-docx not available for DOCX reading")
            return ""
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {str(e)}")
            return ""
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace and normalize line breaks
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Fix common PDF extraction issues
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
        """Create overlapping text chunks with improved sentence boundaries"""
        text = FastembedProvider._clean_text(text)
        
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundaries first
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
    
    def _search_index(self, index_file: str, query: str, top_k: int, embedding_model: str = DEFAULT_MODEL) -> List[Dict]:
        """Search index for relevant documents using FastEmbed"""
        model = self._initialize_model(embedding_model)
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in index file {index_file}: {str(e)}")
            print("Recreating index...")
            return []
        except Exception as e:
            print(f"Error loading index file {index_file}: {str(e)}")
            return []
        
        if 'chunks' not in index_data or 'embeddings' not in index_data:
            print("Error: Invalid index structure (missing 'chunks' or 'embeddings')")
            return []
        
        saved_model = index_data.get('embedding_model', self.DEFAULT_MODEL)
        chunks_metadata = index_data['chunks']
        embeddings = index_data['embeddings']
        
        if saved_model != embedding_model:
            print(f"Warning: Index was created with model '{saved_model}' but searching with '{embedding_model}'")
            print("Consider recreating the index with force_override for better results")
        
        # Generate query embedding
        query_embedding_raw = list(model.embed([query]))[0]
        query_embedding = query_embedding_raw.tolist() if hasattr(query_embedding_raw, 'tolist') else query_embedding_raw
        
        # Compute cosine similarity scores
        scores_and_indices = []
        for idx, embedding in enumerate(embeddings):
            score = self._cosine_similarity(query_embedding, embedding)
            scores_and_indices.append((score, idx))
        
        scores_and_indices.sort(key=lambda x: x[0], reverse=True)
        top_results = scores_and_indices[:top_k]
        
        results = []
        for rank, (score, idx) in enumerate(top_results, 1):
            result = chunks_metadata[idx].copy()
            result['score'] = float(score)
            result['rank'] = rank
            results.append(result)
        
        return results
    
    def _format_results(self, results: List[Dict], query: str) -> str:
        """Format search results for output"""
        if not results:
            return f"No relevant documents found for query: '{query}'"
        
        output = f"RAG Search Results for: '{query}'\n"
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
