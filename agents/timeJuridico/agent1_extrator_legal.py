from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0.2)

prompt = PromptTemplate(
    input_variables=["texto"],
    template="""
Você é um advogado especializado em contratos de locação.

Extraia os principais pontos do seguinte contrato ou cláusula:

{texto}

Responda com uma lista objetiva, como:
- Duração: ...
- Valor: ...
- Reajuste: ...
- Cláusula de multa: ...
"""
)

chain = prompt | llm

def extrair_pontos_chave(texto: str) -> str:
    return chain.invoke({"texto": texto}).content
