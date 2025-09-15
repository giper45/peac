#!/usr/bin/env python3
"""Test script for RAG provider with GPU support"""

import os
import sys
sys.path.insert(0, '/Users/gx1/Git/Unina/peac')

def test_rag_provider():
    """Test the RAG provider functionality with GPU detection"""
    try:
        from peac.providers.rag import RagProvider
        
        provider = RagProvider()
        
        print(f"RAG Provider initialized with device: {provider.device}")
        
        # Test device detection
        print("\nDevice detection test:")
        print(f"Optimal device detected: {provider._get_optimal_device()}")
        
        # Test model initialization (without loading the full model)
        print("\nTesting model initialization...")
        try:
            model = provider._initialize_model()
            print(f"Model initialized successfully on {provider.device}")
            print(f"Model device: {model.device if hasattr(model, 'device') else 'Not available'}")
        except Exception as e:
            print(f"Model initialization failed: {e}")
        
        print("\nRAG provider test completed!")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure to install dependencies: poetry install")
    except Exception as e:
        print(f"Test error: {e}")

if __name__ == "__main__":
    test_rag_provider()
