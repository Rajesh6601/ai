#!/usr/bin/env python3
"""
Test script for the Himalaya Enterprises web loader tool.
This script tests the functionality of the web loader tool to ensure it can
properly load and search content from the Himalaya Enterprises website.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_himalaya_tool():
    """Test the Himalaya Enterprises web loader tool."""
    try:
        from langgraphagenticai.tools.webloader_tool import get_himalaya_tool
        
        print("Initializing Himalaya Enterprises tool...")
        himalaya_tool = get_himalaya_tool()
        
        print("Tool initialized successfully!")
        print(f"Tool name: {himalaya_tool.name}")
        print(f"Tool description: {himalaya_tool.description}")
        
        # Test queries
        test_queries = [
            "Where is Himalaya Enterprises located?",
            "What services does Himalaya Enterprises provide?",
            "Tell me about Himalaya Enterprises",
            "Contact information for Himalaya Enterprises",
            "What products does Himalaya Enterprises offer?",
            "Tell me about Himalaya Enterprises products",
            "How can I contact Himalaya Enterprises?",
            "What is the phone number of Himalaya Enterprises?",
            "What projects has Himalaya Enterprises completed?",
            "Tell me about Himalaya Enterprises projects"
        ]
        
        print("\n" + "="*50)
        print("Testing queries:")
        print("="*50)
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            print("-" * 40)
            try:
                result = himalaya_tool._run(query)
                print(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n" + "="*50)
        print("Test completed!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_himalaya_tool()
