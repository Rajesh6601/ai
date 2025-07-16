#!/usr/bin/env python3
"""
Test LinkedIn posts query for Himalaya Enterprises tool.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_linkedin_posts_query():
    """Test LinkedIn posts specific query."""
    try:
        from langgraphagenticai.tools.webloader_tool import get_himalaya_tool
        
        print("Initializing Himalaya Enterprises tool...")
        himalaya_tool = get_himalaya_tool()
        
        # Test the specific query from the user
        test_query = "what is the latest post by himalaya enterprises in linkedin?"
        
        print(f"\nTesting query: {test_query}")
        print("="*80)
        
        result = himalaya_tool.run(test_query)
        print(f"Result:\n{result}")
        
    except Exception as e:
        print(f"Error during LinkedIn posts testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_linkedin_posts_query()
