import os
import pickle
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import re

class RagProvider:
    """RAG (Retrieval-Augmented Generation) provider using FAISS for vector search"""
    
    def __init__(self):
        self.embeddings = None
        self.index = None
        self.documents = None
        self.model = None
        self.device = self._get_optimal_device()
    
    def _get_optimal_device(self):
        """Detect and return the optimal device (GPU, MPS, or CPU)"""
        try:
            import torch
            
            # Check for CUDA (NVIDIA GPU)
            if torch.cuda.is_available():
                device = torch.device("cuda")
                print(f"Using CUDA GPU: {torch.cuda.get_device_name(0)}")
                return device
            
            # Check for MPS (Apple Silicon GPU)
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                device = torch.device("mps")
                print("Using Apple Silicon GPU (MPS)")
                return device
            
            # Fallback to CPU
            else:
                device = torch.device("cpu")
                print("Using CPU (no GPU available)")
                return device
                
        except ImportError:
            # PyTorch not available, will use CPU with sentence-transformers default
            print("PyTorch not available, using CPU")
            return "cpu"
    
    def _initialize_model(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the sentence transformer model with optimal device"""
        try:
            from sentence_transformers import SentenceTransformer
            # Always reload model if model_name is different or model is None
            if self.model is None or getattr(self, '_current_model_name', None) != model_name:
                print(f"Loading sentence transformer model: {model_name}")
                self.model = SentenceTransformer(model_name, device=self.device)
                self._current_model_name = model_name
                print(f"Model loaded successfully on {self.device}")
            return self.model
        except ImportError:
            raise ImportError("sentence-transformers library not installed. Install with: pip install sentence-transformers")
    
    def _initialize_faiss(self):
        """Initialize FAISS library"""
        try:
            import faiss
            return faiss
        except ImportError:
            raise ImportError("faiss-cpu library not installed. Install with: pip install faiss-cpu")
    
    def parse(self, faiss_file: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Parse RAG request and return relevant documents
        
        Args:
            faiss_file: Path to the FAISS index file
            options: Dictionary containing:
                - query: Search query for RAG retrieval
                - source_folder: Folder/file to embed if FAISS file doesn't exist
                - top_k: Number of top results to return (default: 5)
                - chunk_size: Size of text chunks for embedding (default: 512)
                - overlap: Overlap between chunks (default: 50)
                - force_override: Force recreation of FAISS index (default: False)
                - embedding_model: Model name for embedding (default: 'all-MiniLM-L6-v2')
        
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
        embedding_model = options.get('embedding_model', 'all-MiniLM-L6-v2')
        
        # Check if FAISS file exists and if we should override it
        should_create_index = force_override or not os.path.exists(faiss_file)
        
        if should_create_index:
            if not source_folder:
                if force_override:
                    return f"Error: Force override enabled but no source folder provided to recreate FAISS index"
                else:
                    return f"Error: FAISS file '{faiss_file}' does not exist and no source folder provided"
            
            if force_override:
                print(f"Force override enabled. Recreating FAISS index: {faiss_file}")
            else:
                print(f"FAISS file '{faiss_file}' not found. Creating from source: {source_folder}")
                
            success = self._create_faiss_index(faiss_file, source_folder, chunk_size, overlap, embedding_model)
            if not success:
                return f"Error: Failed to create FAISS index from {source_folder}"
        
        # Load FAISS index and perform search (using the same model used for creation)
        try:
            results = self._search_faiss(faiss_file, query, top_k, embedding_model)
            return self._format_results(results, query)
        except Exception as e:
            return f"Error during RAG search: {str(e)}"
    
    def _create_faiss_index(self, faiss_file: str, source_folder: str, chunk_size: int, overlap: int, embedding_model: str = 'all-MiniLM-L6-v2') -> bool:
        """Create FAISS index from source folder/file"""
        try:
            faiss = self._initialize_faiss()
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
            
            print(f"Created {len(chunks)} chunks. Generating embeddings...")
            
            # Generate embeddings with batch processing for GPU efficiency
            # Adjust batch size based on device capabilities
            if str(self.device) == "cuda":
                batch_size = 64  # Larger batch for CUDA
            elif str(self.device) == "mps":
                batch_size = 32  # Medium batch for Apple Silicon
            else:
                batch_size = 16  # Smaller batch for CPU
                
            print(f"Using batch size: {batch_size} for device: {self.device}")
            
            try:
                embeddings = model.encode(
                    chunks, 
                    show_progress_bar=True,
                    batch_size=batch_size,
                    convert_to_tensor=True,
                    normalize_embeddings=True
                )
            except Exception as e:
                if "out of memory" in str(e).lower() or "memory" in str(e).lower():
                    print(f"GPU memory error, falling back to smaller batch size...")
                    batch_size = max(1, batch_size // 2)
                    embeddings = model.encode(
                        chunks, 
                        show_progress_bar=True,
                        batch_size=batch_size,
                        convert_to_tensor=True,
                        normalize_embeddings=True
                    )
                else:
                    raise e
            
            # Create FAISS index
            # Convert tensor to numpy if needed
            if hasattr(embeddings, 'cpu'):
                embeddings_np = embeddings.cpu().numpy()
            else:
                embeddings_np = embeddings
                
            dimension = embeddings_np.shape[1]
            index = faiss.IndexFlatIP(dimension)  # Inner product similarity
            
            # Normalize embeddings for cosine similarity (if not already normalized)
            if not hasattr(embeddings, 'cpu'):  # If not from tensor (already normalized)
                faiss.normalize_L2(embeddings_np)
            
            index.add(embeddings_np)
            
            # Save FAISS index and metadata
            faiss_dir = os.path.dirname(faiss_file)
            if faiss_dir:
                os.makedirs(faiss_dir, exist_ok=True)
            
            faiss.write_index(index, faiss_file)
            
            # Save metadata including model information
            metadata_file = faiss_file.replace('.faiss', '_metadata.json')
            metadata_with_info = {
                'embedding_model': embedding_model,
                'chunks': chunk_metadata
            }
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata_with_info, f, ensure_ascii=False, indent=2)
            
            print(f"FAISS index created successfully: {faiss_file}")
            print(f"Metadata saved: {metadata_file}")
            print(f"Used embedding model: {embedding_model}")
            return True
            
        except Exception as e:
            print(f"Error creating FAISS index: {str(e)}")
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
    
    def _is_text_file(self, file_path: Path) -> bool:
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
    
    def _read_pdf(self, file_path: str) -> str:
        """Read PDF content using pdfplumber"""
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return self._clean_text(text)
        except ImportError:
            print("pdfplumber not available for PDF reading")
            return ""
        except Exception as e:
            print(f"Error reading PDF {file_path}: {str(e)}")
            return ""
    
    def _read_docx(self, file_path: str) -> str:
        """Read DOCX content"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return self._clean_text(text)
        except ImportError:
            print("python-docx not available for DOCX reading")
            return ""
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {str(e)}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        import re
        
        # Remove excessive whitespace and normalize line breaks
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Normalize paragraph breaks
        
        # Fix common PDF extraction issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between camelCase
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)  # Add space after sentence endings
        text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)  # Join hyphenated words split across lines
        text = re.sub(r'(\w)\n(\w)', r'\1 \2', text)  # Join words split across lines
        
        # Clean up specific patterns from your example
        text = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', text)  # Fix: "rityobjectives,asthereisno" -> "rity objectives, as there is no"
        text = re.sub(r'(\w)([A-Z]+)(\w)', r'\1 \2 \3', text)  # Fix: "wordWORDword" -> "word WORD word"
        
        # Remove extra spaces and normalize
        text = ' '.join(text.split())
        
        return text
    
    def _create_chunks(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Create overlapping text chunks with improved sentence boundaries"""
        # Clean the text first
        text = self._clean_text(text)
        
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundaries first
            if end < len(text):
                # Look for sentence endings
                sentence_end = max(
                    chunk.rfind('. '),
                    chunk.rfind('! '),
                    chunk.rfind('? ')
                )
                
                # If no sentence boundary found, try paragraph break
                if sentence_end < chunk_size * 0.6:
                    sentence_end = chunk.rfind('\n\n')
                
                # Fall back to word boundary
                if sentence_end < chunk_size * 0.6:
                    sentence_end = chunk.rfind(' ')
                
                # Only break if we found a reasonable position
                if sentence_end > chunk_size * 0.4:
                    chunk = chunk[:sentence_end + 1]
                    end = start + sentence_end + 1
            
            # Clean and add the chunk
            chunk = chunk.strip()
            if len(chunk) > 50:  # Only keep meaningful chunks
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def _search_faiss(self, faiss_file: str, query: str, top_k: int, embedding_model: str = 'all-MiniLM-L6-v2') -> List[Dict]:
        """Search FAISS index for relevant documents"""
        faiss = self._initialize_faiss()
        model = self._initialize_model(embedding_model)
        
        # Load FAISS index
        index = faiss.read_index(faiss_file)
        
        # Load metadata
        metadata_file = faiss_file.replace('.faiss', '_metadata.json')
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata_data = json.load(f)
        
        # Handle both old and new metadata formats
        if isinstance(metadata_data, dict) and 'chunks' in metadata_data:
            # New format with model information
            saved_model = metadata_data.get('embedding_model', 'all-MiniLM-L6-v2')
            chunks_metadata = metadata_data['chunks']
            
            # Warning if different model is used
            if saved_model != embedding_model:
                print(f"Warning: FAISS index was created with model '{saved_model}' but searching with '{embedding_model}'")
                print("This may lead to suboptimal results. Consider recreating the index with force override.")
        else:
            # Old format - assume default model
            chunks_metadata = metadata_data
            saved_model = 'all-MiniLM-L6-v2'
        
        # Generate query embedding with GPU acceleration
        query_embedding = model.encode(
            [query], 
            convert_to_tensor=True,
            normalize_embeddings=True
        )
        
        # Convert to numpy for FAISS
        if hasattr(query_embedding, 'cpu'):
            query_embedding_np = query_embedding.cpu().numpy()
        else:
            query_embedding_np = query_embedding
            if not hasattr(query_embedding, 'cpu'):  # If not normalized tensor
                faiss.normalize_L2(query_embedding_np)
        
        # Search
        scores, indices = index.search(query_embedding_np, top_k)
        
        # Prepare results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(metadata):
                result = metadata[idx].copy()
                result['score'] = float(score)
                result['rank'] = i + 1
                results.append(result)
        
        return results
    
    def _format_results(self, results: List[Dict], query: str) -> str:
        """Format search results for output with improved text formatting"""
        if not results:
            return f"No relevant documents found for query: '{query}'"
        
        output = f"RAG Search Results for: '{query}'\n"
        output += f"Device used: {self.device}\n"
        output += "=" * 50 + "\n\n"
        
        for result in results:
            output += f"Rank {result['rank']} (Score: {result['score']:.3f})\n"
            output += f"Source: {result['source']}\n"
            output += f"Chunk ID: {result['chunk_id']}\n"
            output += "-" * 30 + "\n"
            
            # Clean and format the text content
            text = result['text']
            
            # Apply additional cleaning for display
            text = self._clean_display_text(text)
            
            # Limit text length but try to break at sentence boundaries
            if len(text) > 500:
                truncated = text[:500]
                last_sentence = max(
                    truncated.rfind('. '),
                    truncated.rfind('! '),
                    truncated.rfind('? ')
                )
                if last_sentence > 300:  # If we found a reasonable sentence break
                    text = truncated[:last_sentence + 1]
                else:
                    text = truncated + "..."
            
            output += text + "\n"
            output += "=" * 50 + "\n\n"
        
        return output
    
    def _clean_display_text(self, text: str) -> str:
        """Additional cleaning for display purposes"""
        import re
        
        # Fix common display issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # camelCase spacing
        text = re.sub(r'(\w)([.!?])([A-Z])', r'\1\2 \3', text)  # Sentence spacing
        text = re.sub(r'([a-z])([A-Z][a-z]+)', r'\1 \2', text)  # Word boundaries
        
        # Fix the specific patterns from your example
        text = re.sub(r'([a-z])([A-Z][a-z]+)([a-z])([A-Z])', r'\1 \2 \3 \4', text)
        
        # Ensure proper paragraph formatting
        text = re.sub(r'\s+', ' ', text)  # Normalize spaces
        text = text.strip()
        
        return text
    
    def apply_filter(self, text: str, filter_regex: str) -> str:
        """
        Apply regex filter to retrieved text
        
        Args:
            text: Retrieved text content
            filter_regex: Regex pattern to match lines
            
        Returns:
            Filtered text content
        """
        if not filter_regex:
            return text
            
        try:
            pattern = re.compile(filter_regex, re.MULTILINE)
            lines = text.split('\n')
            filtered_lines = [line for line in lines if pattern.search(line)]
            return '\n'.join(filtered_lines)
        except re.error:
            # If regex is invalid, return original text
            return text
