import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

class ResourcesAgent:
    def __init__(self):
        load_dotenv()
        self.model = "llama3.2"
        self.llm = ChatOllama(model=self.model, temperature = 0.5)

        self.system_prompts = {"update_query":"""
                You are Aurora, an expert query analizer. You are focused on provideing assitance to Women in accessing resources about safty, infomration and health. Make the query fetch resources and guidance than news. Update the following search query to meet these requirments

                ## Input:
                    - Query: A user search query to be used for searching for web.
                ## Output Format:
                Please output your result exactly as follows without any additional commentary:
                ```json
                {
                "updated_query": "<your update query here>",
                }
                """, 
                "filter_search_results":"""
                    ## ** Goal:**  
                        You are an **AI-powered search result processor** that **filters and ranks** search results based on source trustworthiness. Given a list of search results in JSON format, your task is to **prioritize** and **sort** them, ensuring that results from **trusted sources** appear first.  

                        ---

                        ## ** System Instructions:**  

                        You are an expert search assistant that processes search results based on **source credibility** and **relevance**. Your goal is to **filter out unreliable sources** and **rank trusted sources higher**.  

                        ### ** Guidelines for Sorting Search Results:**
                        1. ** Highest Priority: Government & Educational Websites**  
                        - Rank results **higher** if they come from **official** domains such as:
                            - `.gov` (Government websites)  
                            - `.edu` (University websites)  
                            - `.org` (Non-profit organizations with credibility, such as WHO, UN, IEEE)
                            - Recognized research institutions  
                        - These are considered the most **reliable and authoritative** sources.

                        2. ** Medium Priority: Established News & Industry Leaders**  
                        - Trusted news sources (e.g., BBC, Reuters, NYTimes).  
                        - Well-known organizations and research-based companies.  
                        - If a `.com` or `.net` source appears credible (e.g., a publication from **Nature.com**, **MIT Technology Review**, or **Harvard Business Review**), it should still be included but **ranked below** government or university sources.  

                        3. **⚠️ Low Priority / Filter Out: Untrusted Sources**  
                        - **Exclude** search results from:
                            - **User-generated content** (e.g., personal blogs, forums like Quora, Reddit, Medium).
                            - **Unverified sources** with potential misinformation.
                            - **SEO-driven websites** with thin content and no citations.
                        - If a search result **does not appear authoritative**, discard it.

                        ### ** Output Format:**  
                        You will return a **filtered and sorted JSON array** where the most trusted sources appear **first**.  
                        Please output your result exactly as the json array below without any additional commentary:
                        
                        ---

                        ## ** Example Input:**
                        [
                            {
                                "url": "https://randomblog.com/article123",
                                "content": "A blog post discussing the topic..."
                            },
                            {
                                "url": "https://www.nasa.gov/news/ai-research",
                                "content": "NASA's latest research on AI and space exploration."
                            },
                            {
                                "url": "https://university.edu/research/ai",
                                "content": "A university study on artificial intelligence."
                            },
                            {
                                "url": "https://randomnews.com/article456",
                                "content": "An unverified news source on AI."
                            }
                        ]
                """}
        self.output_parser = {
            "updated_query":
                StructuredOutputParser.from_response_schemas([
                    ResponseSchema(
                        name="updated_query",
                        description="An updated search query."
                    )
                    ]),
            "filtered_search_results": StructuredOutputParser.from_response_schemas([
                    ResponseSchema(
                        name="filter_search_results",
                        description="Sorted and filtered result."
                    )
                    ]),
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
            search_results = self.tavily_search.invoke(update_query['updated_query'])
            result = self.llm.invoke([
                [ "system", self.system_prompts["filter_search_results"] ],
                [ "human", f"Result: {str(search_results)}"]
            ])

            filtered_result = result.content
        except Exception as e:
            print("Error: ", e)
            return ""
        
        return filtered_result