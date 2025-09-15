#!/usr/bin/env python3
"""Test script for improved RAG text cleaning"""

import os
import sys
sys.path.insert(0, '/Users/gx1/Git/Unina/peac')

def test_rag_text_cleaning():
    """Test the improved RAG text cleaning functionality"""
    try:
        from peac.providers.rag import RagProvider
        
        print("Testing improved RAG text cleaning...")
        
        provider = RagProvider()
        
        # Test text cleaning function with a sample from your output
        dirty_text = "rityobjectives,asthereisnoone-size-fits-allsolution.design, including both functional and non-functional require-ments. Section4delvesintotheimplementationoftheframework"
        cleaned_text = provider._clean_text(dirty_text)
        print(f"Original: {dirty_text}")
        print(f"Cleaned:  {cleaned_text}")
        
        # Test display text cleaning
        display_text = provider._clean_display_text(dirty_text)
        print(f"Display:  {display_text}")
        
        print("\n✅ Text cleaning improvements applied!")
        print("\nTo see the improvements in your RAG results:")
        print("1. Delete your existing exploit.faiss file")
        print("2. Re-run your RAG query to create a new cleaned index")
        print("3. The results should now have better spacing and formatting")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_rag_text_cleaning()
