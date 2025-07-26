"""
LangSmith configuration for debugging and monitoring
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_langsmith():
    """Configure LangSmith for tracing and monitoring"""
    
    # Set LangSmith environment variables
    langsmith_config = {
        "LANGCHAIN_TRACING_V2": "true",
        "LANGCHAIN_ENDPOINT": "https://api.smith.langchain.com",
        "LANGCHAIN_PROJECT": "himalaya-enterprises-chatbot",
    }
    
    # Get LangSmith API key from environment (prefer UI/session)
    langsmith_api_key = os.environ.get("LANGSMITH_API_KEY", "")
    if langsmith_api_key:
        langsmith_config["LANGCHAIN_API_KEY"] = langsmith_api_key
        # Set environment variables
        for key, value in langsmith_config.items():
            os.environ[key] = value
        print("✅ LangSmith tracing enabled")
        print(f"📊 Project: {langsmith_config['LANGCHAIN_PROJECT']}")
        print(f"🔗 Dashboard: https://smith.langchain.com/o/default/projects/p/{langsmith_config['LANGCHAIN_PROJECT']}")
        return True
    else:
        print("⚠️  LangSmith API key not found in environment variables")
        print("📝 Add LANGSMITH_API_KEY in the UI or as an environment variable to enable tracing")
        return False

def get_langsmith_config():
    """Get LangSmith configuration status"""
    return {
        "enabled": os.getenv("LANGCHAIN_TRACING_V2") == "true",
        "project": os.getenv("LANGCHAIN_PROJECT", "himalaya-enterprises-chatbot"),
        "endpoint": os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"),
        "api_key_set": bool(os.getenv("LANGSMITH_API_KEY"))
    }

if __name__ == "__main__":
    # Test the configuration
    config = get_langsmith_config()
    print("LangSmith Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
