from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.9,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

template = """Você é um especialista em SEO e Copywriting no LinkedIn. Otimize o seguinte texto para LinkedIn, usando palavras-chave, emojis e formatação atrativa:

Texto base:
{raw_text}

Texto otimizado para LinkedIn:"""

prompt = PromptTemplate(template=template, input_variables=["raw_text"])
chain = LLMChain(llm=llm, prompt=prompt)

def run_seo_agent(text: str) -> str:
    return chain.run(raw_text=text)
