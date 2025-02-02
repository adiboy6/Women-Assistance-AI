import re
import os
from dotenv import load_dotenv
from typing import List, Annotated, Literal, TypedDict
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain.schema import HumanMessage,AIMessage

from langchain.output_parsers import StructuredOutputParser, ResponseSchema

class AggregatorAgent:
    def __init__(self):
        self.model = "llama3.2"

        self.system_prompt = """
                You are Aurora, You are an expert in aggregating results from search about woment saftey.
                You will be provided a query and one or more of the reponses and your task is to generate an aggregated response in markdown fomrat.
                Aggregate the content of the responses to provide a comprehensive overview of the location/jobs available. 
                Try to give a comprehensive highlight than simple list of resources.

                ## Input
                    - Query: A user query that was supplied to get these responses.
                    - Response: 
                        - A list of resources in a form of url to the source of information and content of the information. 
                        - A list of job reelated information in a form of url to the source of information and content of the information.
                        - A list of location related information in a form of url to the source of information and content of the information.
                        
                    
                ## Output Format:
                Please output an aggregate of these results in a markdown fomrat without any additional commentary. Include the link to each resposne when the URL is provided.
                
                """
        
        self.llm = ChatOllama(model=self.model, temperature = 0.1)

    def run(self, user_input: str, response: List[str]) -> str:
        result = self.llm.invoke([
            [ "system", self.system_prompt ],
            [ "human", f"Query: {user_input}\n Response: {str(response)}"]
            ])
        try:
            return result.content
        except Exception as e:
            return ""
        
if __name__ == "__main__":
    supervisor = AggregatorAgent()
    user_input = "I have a job interview for a Software Engineer position at CNN in downtown Chicago. What can you tell me about the company, local safety, and nearby resources?"
    response = supervisor.run(user_input)
    print(response)