import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

class JobsAgent:
    def __init__(self):
        load_dotenv()
        self.model = "llama3.2"
        self.llm = ChatOllama(model=self.model, temperature = 0.5)

        self.system_prompts = {"update_query":"""
                You are Aurora, an expert query analizer. You are focused on provideing assitance to Women in accessing infomration regarding jobs and companies safty. 
                Update the following search query to be more focused on job posts in the location provided or implied, safty and related information for women in the company if available.
                Make it more focused on jobs and companies that have women's safty information/reports and not about woment's safty jobs.

                ## Input:
                    - Query: A user search query to be used for searching for web.
                ## Output Format:
                Please output your result exactly as follows without any additional commentary:
                ```json
                {
                "updated_query": "<your update query here>",
                }
                """
                }
        self.output_parser = {
            "updated_query":
                StructuredOutputParser.from_response_schemas([
                    ResponseSchema(
                        name="updated_query",
                        description="An updated search query."
                    )
                    ])
            }

        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.tavily_search = TavilySearchResults(api_key=self.tavily_api_key)
    def run(self, query):
        result = self.llm.invoke([
                [ "system", self.system_prompts["update_query"] ],
                [ "human", f"Query: {str(query)}"]
            ])
        try:
            update_query = self.output_parser["updated_query"].parse(result.content)
            search_results = str(self.tavily_search.invoke(update_query['updated_query']))
        except Exception as e:
            print("Error: ", e)
            return ""
        return search_results