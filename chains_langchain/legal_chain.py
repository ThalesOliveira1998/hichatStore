from agents.timeJuridico.agent1_extrator_legal import extrair_pontos_chave
from agents.timeJuridico.agent2_revisor_legal import revisar_contrato
from agents.timeJuridico.agent3_conselheiro_legal import gerar_conselho_legal

def executar_analise_juridica(texto: str) -> dict:
    pontos = extrair_pontos_chave(texto)
    revisao = revisar_contrato(pontos)
    conselho = gerar_conselho_legal(revisao)

    return {
        "pontos_chave": pontos,
        "analise": revisao,
        "conselho": conselho
    }
