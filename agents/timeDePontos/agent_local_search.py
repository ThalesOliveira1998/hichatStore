from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os, json

# Configuração
search = SerpAPIWrapper()
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Prompt que converte o texto em JSON estruturado
prompt = PromptTemplate(
    input_variables=["raw_search", "nicho", "cidade"],
    template="""
Você é um assistente especializado em busca de pontos comerciais para LOCAÇÃO.

Com base na seguinte pesquisa bruta da web:

{raw_search}

Seu objetivo é gerar uma lista com **no mínimo 15 opções de imóveis comerciais para ALUGAR**, relacionadas ao nicho "{nicho}" na cidade de "{cidade}".

Considere imóveis como: lojas, salas comerciais, quiosques, espaços em galerias ou shoppings, coworkings ou outros pontos comerciais.

Ignore imóveis à VENDA e priorize apenas os que estejam disponíveis para ALUGUEL.

Para cada item, responda com os seguintes campos:
- nome
- endereço
- preço (ex: R$ 2.500/mês)
- link do anúncio (ou escreva "Link não disponível")

 Responda **somente com JSON puro**, no seguinte formato:

[
  {{ "nome": "...", "endereco": "...", "preco": "...", "link": "..." }},
  ...
]
"""
)

chain = prompt | llm

def buscar_pontos_comerciais(nicho: str, cidade: str) -> list[dict]:
    consulta = f"Pontos comerciais para {nicho} em {cidade} site:olx.com.br"
    resultados = search.run(consulta)

    resposta = chain.invoke({
        "raw_search": resultados,
        "nicho": nicho,
        "cidade": cidade
    })

    try:
        dados = json.loads(resposta.content)
        if isinstance(dados, list):
            return dados
        else:
            print("❌ Não é uma lista de dicionários")
            return []
    except Exception as e:
        print("❌ Falha ao fazer json.loads:", e)
        print("🔎 Resposta bruta:", resposta.content)
        return []