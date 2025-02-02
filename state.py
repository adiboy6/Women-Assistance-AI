from typing import Annotated, Dict, List, Optional, TypedDict
from typing_extensions import NotRequired
from langgraph.graph.message import add_messages
from langchain.schema import HumanMessage, AIMessage

# ✅ Define State Structure
class State(TypedDict):
    response_supervisor: Annotated[List[AIMessage], add_messages]
    response_location: Annotated[List[AIMessage], add_messages]
    response_resource: Annotated[List[AIMessage], add_messages]
    response_job: Annotated[List[AIMessage], add_messages]
    prompts_supervisor: Annotated[List[AIMessage], add_messages]
    prompts_location: Annotated[List[AIMessage], add_messages]
    prompts_resource: Annotated[List[AIMessage], add_messages]
    prompts_job: Annotated[List[AIMessage], add_messages]
    done:bool