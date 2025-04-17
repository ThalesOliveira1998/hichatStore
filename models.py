from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentePersonalizado:
    nome: str
    instrucoes: str
    criado_por: str
    criado_em: datetime = datetime.now()
