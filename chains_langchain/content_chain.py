from agents.timeConteudo.agent1_researcher import run_research_agent
from agents.timeConteudo.agent2_writer import run_writer_agent
from agents.timeConteudo.agent3_seo import run_seo_agent

def execute_full_chain(user_theme: str):
    research = run_research_agent(user_theme)
    redacao = run_writer_agent(research)
    seo_output = run_seo_agent(redacao)
    return {
        "pesquisa": research,
        "redacao": redacao,
        "seo": seo_output
    }
