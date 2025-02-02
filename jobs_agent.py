import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
class JobsAgent:
    def __init__(self):
        load_dotenv()
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.tavily_search = TavilySearchResults(api_key=self.tavily_api_key)
    def run(self, query):
        search_results = self.tavily_search.invoke(query)
        return search_results