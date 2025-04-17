import csv
import os
from datetime import datetime

def gerar_csv_formatado(dados: list[dict], nome_arquivo="locais"):
    os.makedirs("csv", exist_ok=True)

    agora = datetime.now().strftime("%Y%m%d%H%M%S")
    caminho = f"csv/{nome_arquivo}_{agora}.csv"

    with open(caminho, mode="w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nome", "Endereço", "Preço", "Link"])

        for item in dados:
            nome = item.get("nome", "").strip("[]")
            endereco = item.get("endereco", "").strip("[]")
            preco = item.get("preco", "").strip("[]")
            link = item.get("link", "").strip("[]")
            writer.writerow([nome, endereco, preco, link])

    return caminho
