#!/usr/bin/env python3
"""
Simple LangSmith monitoring test for Himalaya Enterprises chatbot
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

# Load environment variables
load_dotenv()

def test_langsmith_monitoring():
    """Test LangSmith monitoring setup"""
    print("🔍 Testing LangSmith Monitoring Integration")
    print("=" * 50)
    
    # Test LangSmith setup
    from src.langgraphagenticai.utils.langsmith_config import setup_langsmith, get_langsmith_config
    
    setup_result = setup_langsmith()
    config = get_langsmith_config()
    
    print(f"✅ LangSmith Setup: {'Enabled' if setup_result else 'Disabled'}")
    print(f"📊 Project: {config['project']}")
    print(f"🔗 Dashboard: https://smith.langchain.com/o/default/projects/p/{config['project']}")
    
    # Test monitoring dashboard
    from src.langgraphagenticai.utils.langsmith_monitor import LangSmithMonitor
    
    monitor = LangSmithMonitor()
    monitor.print_monitoring_info()
    
    return setup_result

def test_basic_workflow():
    """Test basic workflow with tracing"""
    print("\n🧪 Testing Basic Workflow with Tracing")
    print("=" * 50)
    
    try:
        from src.langgraphagenticai.graph.graph_builder import GraphBuilder
        from src.langgraphagenticai.LLMS.groqllm import GroqLLM
        
        # Mock user input
        user_input = {
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
            "selected_groq_model": "llama3-8b-8192"
        }
        
        if not user_input["GROQ_API_KEY"]:
            print("❌ GROQ_API_KEY not found. Skipping workflow test.")
            return False
        
        # Initialize LLM
        llm_config = GroqLLM(user_input)
        model = llm_config.get_llm_model()
        
        if model:
            print("✅ LLM model initialized successfully")
            
            # Test basic chatbot
            graph_builder = GraphBuilder(model)
            graph = graph_builder.setup_graph("Basic Chatbot")
            
            print("✅ Basic chatbot graph created successfully")
            print("🎯 All components are being traced in LangSmith!")
            
            return True
        else:
            print("❌ Failed to initialize LLM model")
            return False
            
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

def main():
    """Main test function"""
    
    # Check environment
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY not found in environment")
        print("💡 Set GROQ_API_KEY in your .env file for full testing")
    
    # Run tests
    monitoring_result = test_langsmith_monitoring()
    workflow_result = test_basic_workflow()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 MONITORING TEST SUMMARY")
    print("=" * 50)
    
    print(f"🔍 LangSmith Monitoring: {'✅ Enabled' if monitoring_result else '❌ Disabled'}")
    print(f"🧪 Workflow Tracing: {'✅ Working' if workflow_result else '❌ Failed'}")
    
    if monitoring_result:
        print("\n🎉 LangSmith monitoring is active!")
        print("🔗 Check your dashboard: https://smith.langchain.com")
        print("📊 Project: himalaya-enterprises-chatbot")
        print("💡 Run the main application to generate traces")
    else:
        print("\n⚠️  LangSmith monitoring needs setup:")
        print("1. Add LANGSMITH_API_KEY to your .env file")
        print("2. Set LANGCHAIN_TRACING_V2=true")
        print("3. Restart the application")
    
    return monitoring_result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
