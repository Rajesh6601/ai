#!/usr/bin/env python3
"""
Test LinkedIn integration for Himalaya Enterprises tool.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_linkedin_queries():
    """Test LinkedIn-specific queries."""
    try:
        from langgraphagenticai.tools.webloader_tool import get_himalaya_tool
        
        print("Initializing Himalaya Enterprises tool...")
        himalaya_tool = get_himalaya_tool()
        
        # Test LinkedIn-specific queries
        linkedin_queries = [
            "What is the LinkedIn profile of Himalaya Enterprises?",
            "Tell me about Himalaya Enterprises professional network",
            "How can I connect with Himalaya Enterprises on LinkedIn?",
            "What is the LinkedIn URL for Himalaya Enterprises?",
            "Tell me about Himalaya Enterprises professional services from LinkedIn"
        ]
        
        print("\n" + "="*60)
        print("Testing LinkedIn-specific queries:")
        print("="*60)
        
        for query in linkedin_queries:
            print(f"\nQuery: {query}")
            print("-" * 40)
            result = himalaya_tool.run(query)
            print(f"Result: {result}")
            
    except Exception as e:
        print(f"Error during LinkedIn testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_linkedin_queries()
