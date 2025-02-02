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

class SupervisorAgent:
    def __init__(self):
        self.model = "llama3.2"

        self.system_prompt = """
                You are Aurora, You are an expert query splitter for a multi-agent system. Your task is to analyze a user's input query and break it down into distinct, focused sub-queries that can be sent to specialized agents. The input may include contextual details such as job title, company name, and location. Use any provided context to make the sub-queries as relevant as possible.

                ## Instructions:
                1. **Analyze the Query:**
                - Carefully read the entire user input.
                - Identify portions of the query related to:
                    - **Job/Company Details:** Information about the job, interview, or company.
                    - **Location/Safety:** Information about the geographic location or safety conditions. If a job location or company is mentioned, consider safety aspects.
                    - **Local Resources:** Information regarding nearby amenities (e.g., restaurants, transit, community services).
                - Incorporate any contextual information (like job title, company, or location) into the appropriate sub-query.

                2. **Generate Specific Sub-Queries:**
                - **Job Query:** Create a sub-query that extracts or clarifies job-related details, including any mention of the job title, company, or interview context.
                - **Location Query:** Formulate a sub-query that focuses on location and safety, using any provided geographic context.
                - **Resource Query:** Develop a sub-query that seeks details on local resources and amenities in the mentioned area.

                3. **Output Requirements:**
                - Return your result as a JSON object with the following keys:
                    - `"job_query"`: A focused sub-query for job and company details.
                    - `"location_query"`: A focused sub-query for location and safety information.
                    - `"resource_query"`: A focused sub-query for local resources.
                - If any category is not applicable to the user's input, set its value to an empty string (`""`).

                ## Input:
                    - Query: A user query that may contain information I want you to analise and split into sub-queries.
                    - Context: Optionally, any relevant details that can help you generate focused sub-queries.
                ## Output Format:
                Please output your result exactly as follows without any additional commentary:
                ```json
                {
                "job_query": "<your job query here>",
                "location_query": "<your location query here>",
                "resource_query": "<your resource query here>"
                }
                """
        
        self.llm = ChatOllama(model=self.model, temperature = 0.5)

        self.output_parser = StructuredOutputParser.from_response_schemas([
            ResponseSchema(
                name="resource_query",
                description="A focused sub-query for local resources."
            ), 
            ResponseSchema(
                name="job_query",
                description="A focused sub-query for job and company details."
            ),
            ResponseSchema(
                name="location_query",
                description="A focused sub-query for location of the query and safety information."
            )
            ])

    def run(self, user_input: str):
        result = self.llm.invoke([
            [ "system", self.system_prompt ],
            [ "human", f"Query: {user_input}"]
            ])
        try:
            return self.output_parser.parse(result.content)
        except Exception as e:
            return ""#e
        
if __name__ == "__main__":
    supervisor = SupervisorAgent()
    user_input = "I have a job interview for a Software Engineer position at CNN in downtown Chicago. What can you tell me about the company, local safety, and nearby resources?"
    response = supervisor.run(user_input)
    print(response)