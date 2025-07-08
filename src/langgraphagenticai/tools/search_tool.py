from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """ 
    Returns the number of tools to be used in the chatbot 
    """
    tools = [TavilySearchResults(max_results=2)]
    return tools

def create_tool_node(tools):
    """
    Create the langgraph node for the tool use 
    """
    return ToolNode(tool= tools)

