from fastapi import APIRouter
from pydantic import BaseModel
from chains_langchain.content_chain import execute_full_chain
from chains_langchain.legal_chain import executar_analise_juridica
from chains_langchain.location_chain import executar_location_chain


router = APIRouter()

# 📚 MODELOS
class TemaInput(BaseModel):
    tema: str

class ContratoInput(BaseModel):
    texto: str

class LocalizacaoInput(BaseModel):
    nicho: str
    cidade: str
    valor_maximo: int

# 🚀 ROTAS DE EXECUÇÃO

@router.post("/conteudo")
def gerar_conteudo_completo(dados: TemaInput):
    """
    Executa a cadeia de agentes de conteúdo (pesquisa, redação e SEO).
    """
    resultado = execute_full_chain(dados.tema)
    return {"resultado": resultado}


@router.post("/juridico")
def analisar_contrato(dados: ContratoInput):
    """
    Executa a cadeia de análise jurídica (extração, revisão, conselho).
    """
    resultado = executar_analise_juridica(dados.texto)
    return {"resultado": resultado}


@router.post("/localizacao")
def buscar_pontos(dados: LocalizacaoInput):
    """
    Executa a busca por pontos comerciais e retorna o caminho do CSV.
    """
    try:
        csv_path = executar_location_chain(dados.nicho, dados.cidade, dados.valor_maximo)
        return {"csv_path": csv_path}
    except Exception as e:
        return {"erro": str(e)}
