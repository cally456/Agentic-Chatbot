from typing_extensions import TypedDict
from typing import Annotated, List
from langgraph.graph.message import add_messages


class State(TypedDict):
    """
   Represent  the structure of the state in the graph. 
    """
    messages: Annotated[List, add_messages]
