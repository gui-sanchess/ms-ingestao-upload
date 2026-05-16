from abc import ABC, abstractmethod
from typing import List
from domain.entities import Artefato

class ArtefatoRepositoryPort(ABC):
    @abstractmethod
    def salvar(self, artefato: Artefato) -> Artefato:
        pass

    @abstractmethod
    def buscar_por_projeto(self, projeto_id: int) -> List[Artefato]:
        pass

class FileExtractorPort(ABC):
    @abstractmethod
    def extrair_texto(self, conteudo_bytes: bytes, nome_arquivo: str) -> str:
        pass

class IaClientPort(ABC):
    """Porta para comunicação externa com o microsserviço de IA"""
    @abstractmethod
    async def classificar_documento(self, texto: str) -> dict:
        pass