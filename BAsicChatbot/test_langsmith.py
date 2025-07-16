#!/usr/bin/env python3
"""
Test LangSmith integration for Himalaya Enterprises tool.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_langsmith_integration():
    """Test LangSmith integration with the Himalaya Enterprises tool."""
    try:
        from langgraphagenticai.utils.langsmith_config import setup_langsmith, get_langsmith_config
        from langgraphagenticai.tools.webloader_tool import get_himalaya_tool
        
        print("🔧 Testing LangSmith Configuration...")
        print("=" * 50)
        
        # Setup LangSmith
        langsmith_enabled = setup_langsmith()
        
        # Get configuration status
        config = get_langsmith_config()
        print(f"✅ LangSmith Enabled: {config['enabled']}")
        print(f"📊 Project: {config['project']}")
        print(f"🔗 Endpoint: {config['endpoint']}")
        print(f"🔑 API Key Set: {config['api_key_set']}")
        
        if langsmith_enabled:
            print("\n🚀 Testing tool with LangSmith tracing...")
            print("=" * 50)
            
            # Initialize tool (this will be traced)
            himalaya_tool = get_himalaya_tool()
            
            # Test queries (these will be traced)
            test_queries = [
                "What is Himalaya Enterprises?",
                "List the machine names",
                "What is the LinkedIn profile?",
            ]
            
            for query in test_queries:
                print(f"\n🔍 Query: {query}")
                print("-" * 30)
                result = himalaya_tool.run(query)
                print(f"✅ Result: {result[:200]}...")
                
            print(f"\n📊 View traces at: https://smith.langchain.com/o/default/projects/p/{config['project']}")
            
        else:
            print("\n⚠️  LangSmith not enabled. Add LANGSMITH_API_KEY to .env file to enable tracing.")
            
    except Exception as e:
        print(f"❌ Error during LangSmith testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_langsmith_integration()
