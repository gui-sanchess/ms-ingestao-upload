from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from infrastructure.dependency_injection import get_processar_upload_use_case, get_repository
from application.use_cases import ProcessarUploadUseCase
from adapters.outbound.db_repository import PostgresArtefatoRepository

router = APIRouter()


# --- ROTA DE UPLOAD (POST) ---
@router.post("/api/upload")
async def upload_arquivo(
        projeto_id: int = Form(...),
        documento: UploadFile = File(...),
        # A INJEÇÃO ACONTECE AQUI:
        use_case: ProcessarUploadUseCase = Depends(get_processar_upload_use_case)
):
    if not documento.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas PDF permitidos.")

    try:
        conteudo_bytes = await documento.read()

        # Olha que limpeza! Apenas chamamos o maestro, as ferramentas já vieram injetadas.
        artefato_salvo = await use_case.executar(conteudo_bytes, documento.filename, projeto_id)

        return {
            "mensagem": "Arquivo processado pela IA e salvo com sucesso!",
            "artefato_id": artefato_salvo.id,
            "projeto_id": artefato_salvo.projeto_id,
            "classificacao": artefato_salvo.tipo_classificado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- ROTA DE LISTAGEM (GET) ---
@router.get("/api/projetos/{projeto_id}/artefatos")
async def listar_artefatos_por_projeto(
        projeto_id: int,
        # A INJEÇÃO ACONTECE AQUI:
        repository: PostgresArtefatoRepository = Depends(get_repository)
):
    try:
        artefatos = repository.buscar_por_projeto(projeto_id)

        if not artefatos:
            return {"projeto_id": projeto_id, "artefatos": [], "total": 0}

        return {
            "projeto_id": projeto_id,
            "total": len(artefatos),
            "artefatos": [
                {
                    "id": a.id,
                    "nome_arquivo": a.nome_arquivo,
                    "tipo": a.tipo_classificado,
                    "tags": a.tags,
                    "resumo": a.resumo,
                    "data_upload": a.data_upload.isoformat()  # Formata a data bonitinha
                } for a in artefatos
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados: {str(e)}")

@router.delete("/api/artefatos/{artefato_id}")
async def deletar_artefato(
    artefato_id: int,
    repository: PostgresArtefatoRepository = Depends(get_repository)
):
    sucesso = repository.deletar(artefato_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    return {"mensagem": "Arquivo deletado com sucesso!"}