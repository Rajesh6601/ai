from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from .webloader_tool import get_himalaya_tool

def get_tools():
    """
    Return the list of tools to be used in the chatbot
    """
    tools = [
        TavilySearchResults(max_results=2),
        get_himalaya_tool()
    ]
    return tools

def create_tool_node(tools):
    """
    creates and returns a tool node for the graph
    """
    return ToolNode(tools=tools)
