from typing import Annotated, Any, Literal, TypedDict
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage


class State(TypedDict):
    """
    Presents tthe structure of the graph to be used in the graph
    """
    messages: Annotated[list,add_messages]