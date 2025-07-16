#!/usr/bin/env python3
"""
Test machines document integration for Himalaya Enterprises tool.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_machines_queries():
    """Test machine-specific queries."""
    try:
        from langgraphagenticai.tools.webloader_tool import get_himalaya_tool
        
        print("Initializing Himalaya Enterprises tool with machines document...")
        himalaya_tool = get_himalaya_tool()
        
        # Test machine-specific queries
        machine_queries = [
            "Please list the machine names",
            "What machines does Himalaya Enterprises use?",
            "Give me the list of machinery",
            "What equipment is available?",
            "Show me the machines with their quantities",
            "Tell me about the machinery descriptions",
            "What are the machineries used?",
            "List all machines with their numbers"
        ]
        
        print("\n" + "="*80)
        print("Testing machine-specific queries:")
        print("="*80)
        
        for query in machine_queries:
            print(f"\nQuery: {query}")
            print("-" * 60)
            result = himalaya_tool.run(query)
            print(f"Result: {result}")
            print("\n" + "="*80)
            
    except Exception as e:
        print(f"Error during machine testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_machines_queries()
