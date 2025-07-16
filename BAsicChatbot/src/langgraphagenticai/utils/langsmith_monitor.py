"""
LangSmith Monitoring Dashboard Configuration

This module provides utilities for monitoring and debugging the Himalaya Enterprises
chatbot using LangSmith's tracing and analytics capabilities.
"""

import os
from typing import Dict, Any, Optional

class LangSmithMonitor:
    """
    LangSmith monitoring and debugging utilities
    """
    
    def __init__(self):
        self.project_name = "himalaya-enterprises-chatbot"
        self.base_url = "https://smith.langchain.com"
        
    def get_dashboard_url(self) -> str:
        """Get the LangSmith dashboard URL for this project"""
        return f"{self.base_url}/o/default/projects/p/{self.project_name}"
    
    def get_traces_url(self) -> str:
        """Get the traces URL for this project"""
        return f"{self.base_url}/o/default/projects/p/{self.project_name}/traces"
    
    def get_analytics_url(self) -> str:
        """Get the analytics URL for this project"""
        return f"{self.base_url}/o/default/projects/p/{self.project_name}/analytics"
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get comprehensive monitoring configuration"""
        return {
            "project_name": self.project_name,
            "dashboard_url": self.get_dashboard_url(),
            "traces_url": self.get_traces_url(),
            "analytics_url": self.get_analytics_url(),
            "tracing_enabled": os.getenv("LANGCHAIN_TRACING_V2") == "true",
            "api_key_configured": bool(os.getenv("LANGSMITH_API_KEY")),
            "traced_components": [
                "WebLoader Tool",
                "Graph Builder",
                "Basic Chatbot Node",
                "Chatbot with Tools Node",
                "LLM Model",
                "Display Result UI",
                "Main Application"
            ]
        }
    
    def print_monitoring_info(self):
        """Print monitoring information to console"""
        config = self.get_monitoring_config()
        
        print("🔍 LangSmith Monitoring Dashboard")
        print("=" * 50)
        print(f"📊 Project: {config['project_name']}")
        print(f"🔗 Dashboard: {config['dashboard_url']}")
        print(f"📈 Traces: {config['traces_url']}")
        print(f"📊 Analytics: {config['analytics_url']}")
        print(f"✅ Tracing: {'Enabled' if config['tracing_enabled'] else 'Disabled'}")
        print(f"🔑 API Key: {'Configured' if config['api_key_configured'] else 'Not Configured'}")
        print("\n📋 Traced Components:")
        for component in config['traced_components']:
            print(f"  • {component}")
        
        if config['tracing_enabled'] and config['api_key_configured']:
            print("\n🎉 LangSmith monitoring is fully configured!")
            print("💡 Run the application and check the dashboard for traces")
        else:
            print("\n⚠️  LangSmith monitoring needs configuration:")
            if not config['api_key_configured']:
                print("  • Add LANGSMITH_API_KEY to your .env file")
            if not config['tracing_enabled']:
                print("  • Ensure LANGCHAIN_TRACING_V2=true in environment")

def get_trace_metadata(operation_name: str, **kwargs) -> Dict[str, Any]:
    """
    Get metadata for LangSmith traces
    
    Args:
        operation_name: Name of the operation being traced
        **kwargs: Additional metadata
    
    Returns:
        Dict containing trace metadata
    """
    metadata = {
        "operation": operation_name,
        "application": "himalaya-enterprises-chatbot",
        "component": kwargs.get("component", "unknown"),
        "version": "1.0.0"
    }
    
    # Add additional metadata
    metadata.update(kwargs)
    
    return metadata

def trace_error(error: Exception, operation_name: str, **kwargs):
    """
    Trace errors with LangSmith
    
    Args:
        error: The exception that occurred
        operation_name: Name of the operation where error occurred
        **kwargs: Additional context
    """
    metadata = get_trace_metadata(operation_name, **kwargs)
    metadata.update({
        "error_type": type(error).__name__,
        "error_message": str(error),
        "status": "error"
    })
    
    # In a real implementation, this would send to LangSmith
    print(f"❌ Error traced: {operation_name} - {error}")
    return metadata

# Usage examples and help text
USAGE_EXAMPLES = """
🔧 LangSmith Usage Examples:

1. Basic Setup:
   ```python
   from utils.langsmith_config import setup_langsmith
   setup_langsmith()
   ```

2. View Monitoring Info:
   ```python
   from utils.langsmith_monitor import LangSmithMonitor
   monitor = LangSmithMonitor()
   monitor.print_monitoring_info()
   ```

3. Trace Custom Functions:
   ```python
   from langsmith import traceable
   
   @traceable(name="my_function")
   def my_function(input_data):
       return process_data(input_data)
   ```

4. Check Dashboard:
   - Go to: https://smith.langchain.com
   - Navigate to project: himalaya-enterprises-chatbot
   - View traces, analytics, and performance metrics

🎯 Key Monitoring Features:
• Request/Response tracing
• Performance metrics
• Error tracking
• Token usage analytics
• Component-level debugging
• User interaction flows
"""

if __name__ == "__main__":
    monitor = LangSmithMonitor()
    monitor.print_monitoring_info()
    print(USAGE_EXAMPLES)
