import re
import os
from state import State
from supervisor_agent import SupervisorAgent
from jobs_agent import JobsAgent
from location_agent import LocationAgent
from resources_agent import ResourcesAgent
from dotenv import load_dotenv
from typing import List, Annotated, Literal, TypedDict
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain.schema import HumanMessage,AIMessage
from collections import defaultdict

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

class Orchestrator:
    def __init__(self):
        """
        Initialize the workflow orchestration system
 
        """
        
        self.supervisor_agent = SupervisorAgent()
        self.jobs_agent = JobsAgent()
        self.locations_agent = LocationAgent()
        self.resources_agent = ResourcesAgent()

        # Create LangGraph workflow
        self.workflow = StateGraph(State)

        # Add nodes
        self.workflow.add_node("supervisor", self.supervisor)
        self.workflow.add_node("jobs", self.jobs)
        self.workflow.add_node("location", self.location)
        self.workflow.add_node("resource", self.resource)
        self.workflow.add_node("aggregator", self.aggregator)

        self.workflow.add_conditional_edges(
            "aggregator",
            lambda state: "end" if state.get("done", False) else "continue",
            {
                "end": END,
                "continue": "supervisor"
            }
        )
        # Set entry point
        self.workflow.set_entry_point("supervisor")
        
        self.workflow.add_edge("supervisor", "jobs")
        self.workflow.add_edge("supervisor", "location")
        self.workflow.add_edge("supervisor", "resource")

        self.workflow.add_edge("jobs", "aggregator")
        self.workflow.add_edge("location", "aggregator")
        self.workflow.add_edge("resource", "aggregator")
        # Compile the workflow
        self.app = self.workflow.compile()
        self.app.get_graph().draw_mermaid_png(output_file_path="workflow.png")

    def supervisor(self, state: State) -> State:
        # Get supervisor response
        prompt = state["prompts_supervisor"][-1]
        subqueries = self.supervisor_agent.run(prompt)
        state["prompts_job"].append(AIMessage(subqueries.get('job_query','')))
        state["prompts_location"].append(AIMessage(subqueries.get('location_query','')))
        state["prompts_resource"].append(AIMessage(subqueries.get('resource_query','')))
        return state
    def aggregator(self, state: State) -> State:
        state["done"] = True
        # TODO: validate
        return state
    
    def jobs(self, state: State) -> State:
        prompt = state["prompts_job"][-1]
        if prompt:
            print(prompt)
            self.jobs_agent.run(prompt.content)
            #TODO: parse the response
        return state
    
    def location(self, state: State) -> State:
        prompt = state["prompts_location"][-1]
        if prompt:
            self.locations_agent.run(prompt.content)
            #TODO: parse the response
        return state
    
    def resource(self, state: State) -> State:
        prompt = state["prompts_resource"][-1]
        if prompt:
            self.resources_agent.run(prompt.content)
            #TODO: parse the response
        return state
    
    def start(self, user_input: str) -> str:
        return self.app.invoke({"prompts_supervisor":user_input})  # Start with the initial state
if __name__ == "__main__":
    orchestrator = Orchestrator()
    # while True:
        # user_input = input("You: ")
    user_input = "I have a job interview for a Software Engineer position at CNN in downtown Chicago. What can you tell me about the company, local safety, and nearby resources?"
        # if user_input.lower() == "exit":
        #     print("Chatbot: Goodbye!")
        #     break
    response = orchestrator.start(user_input)
    print(response)