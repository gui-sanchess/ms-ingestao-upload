from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Artefato:
    nome_arquivo: str
    conteudo_extraido: str
    projeto_id: int  # <-- NOVA COLUNA (Obrigatória)
    tipo_classificado: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    resumo: Optional[str] = None
    data_upload: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None