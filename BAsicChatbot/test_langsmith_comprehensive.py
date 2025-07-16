#!/usr/bin/env python3
"""
Comprehensive test for LangSmith integration with Himalaya Enterprises chatbot
Tests all components with tracing enabled
"""

import os
import sys
import uuid
from pathlib import Path
from dotenv import load_dotenv

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

# Load environment variables
load_dotenv()

# Test LangSmith setup
from src.langgraphagenticai.utils.langsmith_config import setup_langsmith, get_langsmith_config

def test_langsmith_setup():
    """Test LangSmith configuration and setup"""
    print("🧪 Testing LangSmith Setup...")
    
    # Test setup
    setup_result = setup_langsmith()
    print(f"Setup result: {setup_result}")
    
    # Get configuration
    config = get_langsmith_config()
    print(f"Configuration: {config}")
    
    return setup_result

def test_graph_builder_tracing():
    """Test GraphBuilder with LangSmith tracing"""
    print("\n🧪 Testing Graph Builder with LangSmith tracing...")
    
    try:
        from src.langgraphagenticai.graph.graph_builder import GraphBuilder
        from src.langgraphagenticai.LLMS.groqllm import GroqLLM
        
        # Mock user input for testing
        user_input = {
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
            "selected_groq_model": "llama3-8b-8192"
        }
        
        # Initialize LLM
        llm_config = GroqLLM(user_input)
        model = llm_config.get_llm_model()
        
        if model:
            # Test graph building with tracing
            graph_builder = GraphBuilder(model)
            
            # Test basic chatbot graph
            print("Building basic chatbot graph...")
            graph = graph_builder.setup_graph("Basic Chatbot")
            print("✅ Basic chatbot graph built successfully")
            
            # Test chatbot with tools graph
            print("Building chatbot with tools graph...")
            graph = graph_builder.setup_graph("Chatbot With Web")
            print("✅ Chatbot with tools graph built successfully")
            
            return True
        else:
            print("❌ Failed to initialize LLM model")
            return False
            
    except Exception as e:
        print(f"❌ Graph builder test failed: {e}")
        return False

def test_webloader_tool_tracing():
    """Test WebLoader tool with LangSmith tracing"""
    print("\n🧪 Testing WebLoader Tool with LangSmith tracing...")
    
    try:
        from src.langgraphagenticai.tools.webloader_tool import WebLoaderTool
        
        # Create tool instance
        tool = WebLoaderTool()
        
        # Test machine search with tracing
        print("Testing machine search...")
        result = tool._run("What machines are available from Himalaya Enterprises?")
        print(f"✅ Machine search result: {result[:200]}...")
        
        # Test web search with tracing
        print("Testing web search...")
        result = tool._run("What is artificial intelligence?")
        print(f"✅ Web search result: {result[:200]}...")
        
        # Test LinkedIn search with tracing
        print("Testing LinkedIn search...")
        result = tool._run("Find LinkedIn posts about AI")
        print(f"✅ LinkedIn search result: {result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ WebLoader tool test failed: {e}")
        return False

def test_nodes_tracing():
    """Test node components with LangSmith tracing"""
    print("\n🧪 Testing Nodes with LangSmith tracing...")
    
    try:
        from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
        from src.langgraphagenticai.nodes.chatbot_with_Tool_node import ChatbotWithToolNode
        from src.langgraphagenticai.LLMS.groqllm import GroqLLM
        
        # Mock user input for testing
        user_input = {
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
            "selected_groq_model": "llama3-8b-8192"
        }
        
        # Initialize LLM
        llm_config = GroqLLM(user_input)
        model = llm_config.get_llm_model()
        
        if model:
            # Test basic chatbot node
            print("Testing basic chatbot node...")
            basic_node = BasicChatbotNode(model)
            
            # Test chatbot with tools node
            print("Testing chatbot with tools node...")
            tools_node = ChatbotWithToolNode(model)
            
            print("✅ Node components initialized successfully")
            return True
        else:
            print("❌ Failed to initialize LLM model")
            return False
            
    except Exception as e:
        print(f"❌ Nodes test failed: {e}")
        return False

def test_end_to_end_tracing():
    """Test end-to-end workflow with LangSmith tracing"""
    print("\n🧪 Testing End-to-End Workflow with LangSmith tracing...")
    
    try:
        from src.langgraphagenticai.graph.graph_builder import GraphBuilder
        from src.langgraphagenticai.LLMS.groqllm import GroqLLM
        
        # Mock user input for testing
        user_input = {
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
            "selected_groq_model": "llama3-8b-8192"
        }
        
        # Initialize LLM
        llm_config = GroqLLM(user_input)
        model = llm_config.get_llm_model()
        
        if model:
            # Build graph
            graph_builder = GraphBuilder(model)
            graph = graph_builder.setup_graph("Chatbot With Web")
            
            # Test query
            test_query = "What machines does Himalaya Enterprises offer?"
            print(f"Testing query: {test_query}")
            
            # Run the graph
            result = graph.invoke({"messages": [test_query]})
            print(f"✅ End-to-end workflow completed successfully")
            print(f"Result type: {type(result)}")
            
            return True
        else:
            print("❌ Failed to initialize LLM model")
            return False
            
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False

def main():
    """Run comprehensive LangSmith integration tests"""
    print("🔧 Comprehensive LangSmith Integration Test")
    print("=" * 50)
    
    # Check if GROQ_API_KEY is available
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please set GROQ_API_KEY in your .env file")
        return False
    
    # Run tests
    tests = [
        test_langsmith_setup,
        test_graph_builder_tracing,
        test_webloader_tool_tracing,
        test_nodes_tracing,
        test_end_to_end_tracing
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n🎉 All LangSmith integration tests passed!")
        print("🔗 Check your LangSmith dashboard at: https://smith.langchain.com")
        print("📊 Project: himalaya-enterprises-chatbot")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
