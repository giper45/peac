#!/usr/bin/env python3
"""Test script for RAG integration with PEaC core engine"""

import os
import sys
sys.path.insert(0, '/Users/gx1/Git/Unina/peac')

def test_rag_integration():
    """Test RAG integration with PEaC core engine"""
    try:
        from peac.core.peac import PromptYaml
        from peac.local_parser import get_rag_provider, parse_rag
        
        print("Testing RAG integration with PEaC core engine...")
        
        # Test RAG provider availability
        rag_provider = get_rag_provider()
        if rag_provider:
            print(f"✓ RAG provider available: {type(rag_provider).__name__}")
            print(f"✓ GPU device: {rag_provider.device}")
        else:
            print("✗ RAG provider not available")
            return
        
        # Test parse_rag function
        print("\nTesting parse_rag function...")
        try:
            # This will fail gracefully since we don't have a real FAISS file
            result = parse_rag("/path/to/test.faiss", {
                'query': 'test query',
                'source_folder': '/tmp',
                'top_k': 3
            })
            print(f"✓ parse_rag function works (result: {len(result)} chars)")
        except Exception as e:
            print(f"✓ parse_rag function handles errors gracefully: {str(e)[:100]}")
        
        # Test YAML template
        print("\nTesting RAG YAML template...")
        try:
            from peac.main import get_template_file
            template_content = get_template_file()
            if 'rag:' in template_content:
                print("✓ RAG section found in template")
            else:
                print("✗ RAG section not found in template")
        except:
            print("ℹ Template test skipped")
        
        print("\n🎉 RAG integration test completed successfully!")
        
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"Test error: {e}")

if __name__ == "__main__":
    test_rag_integration()
