from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0.2)

prompt = PromptTemplate(
    input_variables=["pontos"],
    template="""
Você é um advogado especializado em análise de contratos.

Revise os seguintes pontos contratuais:

{pontos}

Sinalize qualquer cláusula:
- Abusiva
- Mal redigida
- Que pode causar risco jurídico ao locatário

Explique cada problema de forma clara.
"""
)

chain = prompt | llm

def revisar_contrato(pontos: str) -> str:
    return chain.invoke({"pontos": pontos}).content
