from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0.2)
prompt = PromptTemplate(
    input_variables=["analise"],
    template="""
Com base na seguinte análise jurídica:

{analise}

Forneça uma recomendação final simples e objetiva para o cliente, como:

✅ Seguro para assinar  
⚠️ Precisa de ajustes  
❌ Alto risco — não recomendável

Explique brevemente o porquê.
"""
)

chain = prompt | llm

def gerar_conselho_legal(analise: str) -> str:
    return chain.invoke({"analise": analise}).content
