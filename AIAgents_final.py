import os
from tavily import TavilyClient
from pydantic import BaseModel, Field
from typing import List
from crewai.tools import tool
import google.generativeai as genai
from crewai import Agent, Task, LLM ,Crew




os.environ["OPENAI_API_KEY"] = "AIzaSyC1ub0DOeUNv72KYfwivHYNr_ScJIXThCA"
genai.configure(api_key=os.environ["OPENAI_API_KEY"])

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.environ["OPENAI_API_KEY"])



search_client = TavilyClient(api_key="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")
furniture_input = "black sofa"

furniture_listings=search_client.search(furniture_input+":https://www.amazon.eg/")


scraper = Agent(
    llm=llm,
    role="Furniture Recommendation Agent",
    goal=(
        "analyze furniture_listings from amazon of egypt, comparing each product's "
        "specifications against user-defined input criteria to recommend the best match."
    ),
    backstory=(
        "Leveraging advanced web serch techniques and natural language processing, "
        "this agent navigates the amazon platform to extract detailed product specifications "
        "from furniture_listings. It evaluates attributes such as design, dimensions, materials, "
        "and functionality to provide a tailored recommendation based on the provided criteria."
    ),
    allow_delegation=False,
    verbose=False
)

# Define the task to scrape and extract the best matches
plan = Task(
    description=(
       # f"search the manzzeli website for furniture listings. Extract detailed product specifications "
        f"including dimensions, design details, material composition, and functionality. Compare these "
        f"details against the following input criteria: {furniture_listings} "
        "and identify the top  best fit the description."
        "if you don't found any product so say no furniture exist."
        "just show after the( ## Final Answer:) "
        "write just the results"
        "give me the url of each product that you give me in the description"
    ),
    expected_output=(
        "the  best 2 fit furniture with the input description"
        "Each one in desciption format"
        "just print the( ## Final Answer:) "
    ),
    agent=scraper,
)

# Create the crew to run the scraping task
crew = Crew(
    agents=[scraper],
    tasks=[plan],
    verbose=0,
)

result = crew.kickoff()
print(result)