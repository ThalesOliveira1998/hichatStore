import os
import datetime
import requests
import fitz  # PyMuPDF
from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import pandas as pd
import re

# 🧮 CALCULADORA
def tool_calculadora():
    return Tool.from_function(
        func=lambda x: str(eval(x)),
        name="calculadora",
        description="Resolve expressões matemáticas. Ex: '2 + 2'"
    )

# 🕒 HORA ATUAL
def tool_hora_atual():
    return Tool.from_function(
        func=lambda _: f"A hora atual é: {datetime.datetime.now().strftime('%H:%M:%S')}",
        name="hora_atual",
        description="Informa a hora atual do sistema"
    )

# 🔍 BUSCA (com SerpAPI)
def tool_busca():
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_key:
        raise ValueError("Chave da SerpAPI não encontrada.")
    search = SerpAPIWrapper(serpapi_api_key=serpapi_key)
    return Tool.from_function(
        func=search.run,
        name="busca",
        description="Busca informações na internet. Ex: 'O que é LangChain?'"
    )

# 📄 LEITURA DE TXT E PDF
def tool_ler_arquivo():
    def ler(caminho):
        try:
            caminho = caminho.strip()
            print(f"[DEBUG] Lendo: {os.path.abspath(caminho)}")
            if caminho.endswith(".pdf"):
                with open(caminho, "rb") as f:
                    doc = fitz.open(stream=f.read(), filetype="pdf")
                texto = "".join(p.get_text() for p in doc)
                return texto[:1500] or "[PDF vazio]"
            elif caminho.endswith(".txt"):
                with open(caminho, "r", encoding="utf-8") as f:
                    return f.read()[:1500]
            else:
                return "[Formato não suportado. Use .txt ou .pdf]"
        except Exception as e:
            return f"[Erro ao ler o arquivo: {e}]"
    return Tool.from_function(
        func=ler,
        name="ler_arquivo",
        description="Lê arquivos .txt ou .pdf e retorna o conteúdo"
    )

# ☀️ CLIMA (simulado)
def tool_clima():
    return Tool.from_function(
        func=lambda cidade: f"[Simulado] Clima em {cidade.title()} está ensolarado e com 28°C.",
        name="clima",
        description="Informa o clima atual para uma cidade"
    )

# 💱 CONVERSOR DE MOEDA
def tool_conversor_moeda():
    def converter(input_texto: str):
        try:
            partes = input_texto.strip().lower().split()
            valor = float(partes[0])
            de = partes[1].upper()
            para = partes[3].upper()
            url = f"https://economia.awesomeapi.com.br/json/last/{de}-{para}"
            resposta = requests.get(url)
            dados = resposta.json()
            chave = f"{de}{para}"
            taxa = float(dados[chave]["bid"])
            convertido = round(valor * taxa, 2)
            return f"{valor} {de} = {convertido} {para} (cotação: {taxa})"
        except Exception as e:
            return f"[Erro na conversão de moeda: {e}]"
    return Tool.from_function(
        func=converter,
        name="conversor_moeda",
        description="Converte valores entre moedas. Ex: '100 USD para BRL'"
    )

def tool_resumo_texto():
    def resumir(texto: str):
        try:
            llm = ChatOpenAI(temperature=0.3)
            prompt = PromptTemplate(
                input_variables=["conteudo"],
                template="Resuma de forma clara e objetiva o seguinte texto:\n\n{conteudo}"
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            return chain.run(conteudo=texto[:2000])  # evita passar textos gigantes
        except Exception as e:
            return f"[Erro ao gerar resumo: {e}]"

    return Tool.from_function(
        func=resumir,
        name="resumo_texto",
        description="Resume textos longos. Ex: 'resuma: [texto]'"
    )

def tool_lista_tarefas():
    def gerar_lista(instrucao: str):
        try:
            llm = ChatOpenAI(temperature=0.3)
            prompt = PromptTemplate(
                input_variables=["instrucao"],
                template=(
                    "Com base na seguinte descrição, gere uma lista clara e organizada de tarefas ou passos a seguir:\n\n"
                    "{instrucao}\n\n"
                    "Formato:\n"
                    "- Tarefa 1\n- Tarefa 2\n..."
                )
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            return chain.run(instrucao=instrucao[:1000])
        except Exception as e:
            return f"[Erro ao gerar lista de tarefas: {e}]"

    return Tool.from_function(
        func=gerar_lista,
        name="lista_tarefas",
        description="Gera uma lista de tarefas com base em um objetivo ou descrição. Ex: 'crie uma lista de tarefas para mudar de casa'."
    )

def tool_leitor_planilha():
    def ler_planilha(caminho: str):
        try:
            df = pd.read_excel(caminho.strip(), engine="openpyxl")
            resumo = f"Planilha carregada com sucesso!\n\nColunas: {', '.join(df.columns)}\n"
            resumo += f"Número de linhas: {len(df)}\n"
            resumo += "\nExemplo de dados:\n"
            resumo += df.head(5).to_string(index=False)
            return resumo
        except Exception as e:
            return f"[Erro ao ler planilha: {e}]"

    return Tool.from_function(
        func=ler_planilha,
        name="leitor_planilha",
        description="Lê uma planilha .xlsx e retorna suas colunas e uma amostra dos dados."
    )

def tool_resumo_financeiro():
    def gerar_resumo(caminho: str):
        try:
            df = pd.read_excel(caminho.strip(), engine="openpyxl")

            # Gerar uma amostra para análise
            colunas = ', '.join(df.columns)
            linhas = df.head(10).to_string(index=False)

            llm = ChatOpenAI(temperature=0.3)
            prompt = PromptTemplate(
                input_variables=["dados", "colunas"],
                template=(
                    "Você é um analista financeiro.\n"
                    "Abaixo estão as colunas da planilha e uma amostra dos dados.\n\n"
                    "Colunas: {colunas}\n\n"
                    "Dados:\n{dados}\n\n"
                    "Gere um resumo financeiro objetivo com base nesses dados."
                )
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            return chain.run(dados=linhas, colunas=colunas)
        except Exception as e:
            return f"[Erro ao gerar resumo financeiro: {e}]"

    return Tool.from_function(
        func=gerar_resumo,
        name="resumo_financeiro",
        description="Gera um resumo interpretativo de uma planilha financeira (.xlsx)"
    )

def tool_extrator_dados():
    def extrair(texto: str):
        try:
            resultados = []

            email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', texto)
            if email:
                resultados.append(f"E-mail: {email[0]}")

            cpf = re.findall(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}', texto)
            if cpf:
                resultados.append(f"CPF: {cpf[0]}")

            telefone = re.findall(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', texto)
            if telefone:
                resultados.append(f"Telefone: {telefone[0]}")

            nome = re.findall(r"nome (?:é|:)?\s?([A-ZÀ-Ú][a-zà-ú]+(?:\s[A-ZÀ-Ú][a-zà-ú]+)+)", texto, re.IGNORECASE)
            if nome:
                resultados.append(f"Nome: {nome[0]}")

            return "\n".join(resultados) if resultados else "[Nenhum dado pessoal identificado]"
        except Exception as e:
            return f"[Erro ao extrair dados: {e}]"

    return Tool.from_function(
        func=extrair,
        name="extrator_dados",
        description="Extrai nome, CPF, e-mail e telefone de um texto"
    )

# 🎯 MAPEAMENTO DE TOOLS POR NOME
def get_tools_por_nomes(nomes: list[str]):
    todas = {
        "calculadora": tool_calculadora(),
        "hora_atual": tool_hora_atual(),
        "busca": tool_busca(),
        "ler_arquivo": tool_ler_arquivo(),
        "clima": tool_clima(),
        "conversor_moeda": tool_conversor_moeda(),
        "resumo_texto": tool_resumo_texto(),
        "lista_tarefas": tool_lista_tarefas(),
        "leitor_planilha": tool_leitor_planilha(),
        "resumo_financeiro": tool_resumo_financeiro(),
        "extrator_dados": tool_extrator_dados(),


    }
    return [todas[nome] for nome in nomes if nome in todas]
