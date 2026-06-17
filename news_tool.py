from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv

import os

load_dotenv()

@tool
def get_news(city : str) -> str:
  """Return the news related to the place"""

  client = TavilyClient(os.getenv("TAVILY_API_KEY"))
  response = client.search(
      query=f"news about {city}",
      search_depth="advanced"
  )

  result = response

  return result