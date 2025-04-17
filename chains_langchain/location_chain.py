from agents.timeDePontos.agent_local_search import buscar_pontos_comerciais
from agents.timeDePontos.agent_csv_exporter import gerar_csv_formatado

def executar_location_chain(nicho: str, cidade: str, valor_maximo: int) -> str:
    print("🔍 Buscando pontos comerciais...")
    dados = buscar_pontos_comerciais(nicho, cidade)

    print("🧪 Resultado bruto:")
    print(dados)
    print("🔢 Quantidade de resultados:", len(dados))

    if not dados:
        raise Exception("Nenhum ponto comercial encontrado.")

    caminho_csv = gerar_csv_formatado(dados)
    print("✅ CSV gerado:", caminho_csv)

    return caminho_csv
