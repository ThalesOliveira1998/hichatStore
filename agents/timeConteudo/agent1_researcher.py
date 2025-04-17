import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain_community.utilities.serpapi import SerpAPIWrapper

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

search = SerpAPIWrapper()

tools = [
    Tool(
        name="Google Search",
        func=search.run,
        description="Busca informações relevantes sobre o tema"
    )
]

def run_research_agent(theme: str) -> str:
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    return agent.run(f"Pesquise sobre o tema: {theme}")
