from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

# Inicializa o LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Prompt para geração de redação
template = """Com base no conteúdo a seguir, crie uma redação estruturada e coerente sobre o tema:

{research_content}

Redação:"""

# Define o prompt template com variável `research_content`
prompt = PromptTemplate(
    input_variables=["research_content"],
    template=template
)

# Novo pipeline com runnable: prompt | llm
chain = prompt | llm

# Função que executa o agente
def run_writer_agent(content: str) -> str:
    response = chain.invoke({"research_content": content})
    return response.content  # Novo: precisa acessar `.content`
