from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))

def filtrar_resultados(texto: str, valor_maximo: int) -> str:
    prompt = f"""
Você é um assistente que analisa pontos comerciais. Abaixo está uma lista de anúncios coletados.

Filtre e formate apenas os 5 melhores pontos com:

- Preço estimado até R$ {valor_maximo}
- Endereço ou bairro (se disponível)
- Nome do local ou título
- Link do anúncio (se houver)

Formato desejado (1 por linha):
[NOME] - [ENDEREÇO/BAIRRO] - [PREÇO] - [LINK]
---
{texto}
"""
    resposta = llm.invoke(prompt)
    return resposta.content
