from fastapi import Depends
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from adapters.outbound.db_repository import PostgresArtefatoRepository
from adapters.outbound.file_extractor import PDFExtractorAdapter
from adapters.outbound.ia_service_client import HttpIaClientAdapter
from application.use_cases import ProcessarUploadUseCase

# 1. Provedores Básicos (Instanciam as ferramentas externas)
def get_repository(db: Session = Depends(get_db)) -> PostgresArtefatoRepository:
    return PostgresArtefatoRepository(db)

def get_file_extractor() -> PDFExtractorAdapter:
    return PDFExtractorAdapter()

def get_ia_client() -> HttpIaClientAdapter:
    return HttpIaClientAdapter()

# 2. Provedor Mestre (Monta o Caso de Uso com todas as ferramentas injetadas)
def get_processar_upload_use_case(
    extractor: PDFExtractorAdapter = Depends(get_file_extractor),
    repository: PostgresArtefatoRepository = Depends(get_repository),
    ia_client: HttpIaClientAdapter = Depends(get_ia_client)
) -> ProcessarUploadUseCase:
    """
    O FastAPI é inteligente o suficiente para rodar as 3 funções acima,
    pegar os resultados e injetar aqui automaticamente.
    """
    return ProcessarUploadUseCase(extractor, repository, ia_client)